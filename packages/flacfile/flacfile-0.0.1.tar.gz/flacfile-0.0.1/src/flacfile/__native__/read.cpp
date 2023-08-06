#include <algorithm>
#include <exception>
#include <functional>
#include <stdexcept>
#include <string>
#include <tuple>

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include <FLAC/stream_decoder.h>

#include <fmt/format.h>
using namespace fmt::literals;

#include "flacfile.h"

namespace py = pybind11;

namespace flacfile {

namespace {
FLAC__StreamDecoderWriteStatus
write_callback(const FLAC__StreamDecoder* decoder, const FLAC__Frame* frame,
               const FLAC__int32* const buffer[], void* client_data);
void metadata_callback(const FLAC__StreamDecoder* decoder,
                       const FLAC__StreamMetadata* metadata, void* client_data);
void error_callback(const FLAC__StreamDecoder* decoder,
                    FLAC__StreamDecoderErrorStatus status, void* client_data);

struct ReaderData {
  py::array samples;
  unsigned sample_rate;
  std::string error_msg;

  uint64_t total_samples;
  uint32_t channels;
  uint32_t bps;

  std::function<int32_t(const int32_t)> justify;
};

template <class T>
void fill_numpy_array(py::array_t<T> out, const uint32_t N, const uint64_t n0,
                      const FLAC__int32* const buffer[],
                      const std::function<int32_t(const int32_t)> justify) {
  auto r = out.mutable_unchecked();

  if (r.ndim() > 1) {
    for (py::ssize_t i = 0; i < N; ++i)            // samples
      for (py::ssize_t j = 0; j < r.shape(1); ++j) // channels
        r(i + n0, j) = justify(buffer[j][i]);
  } else {
    auto buf = buffer[0];
    for (py::ssize_t i = 0; i < N; ++i)
      r(i + n0) = justify(buf[i]);
  }
}

FLAC__StreamDecoderWriteStatus
write_callback(const FLAC__StreamDecoder* decoder, const FLAC__Frame* frame,
               const FLAC__int32* const buffer[], void* client_data) {
  ReaderData& data = *(ReaderData*)client_data;
  const FLAC__FrameHeader& header = frame->header;
  uint64_t n0 = header.number.sample_number; // always sample index for decoder
  uint32_t N = header.blocksize;

  if (header.channels != data.channels) {
    data.error_msg = "ERROR: A frame containing unexpected number of channels.";
    return FLAC__STREAM_DECODER_WRITE_STATUS_ABORT;
  }

  if (n0 + N > data.total_samples) {
    data.error_msg =
        "ERROR: A frame containing samples beyond the expected total.";
    return FLAC__STREAM_DECODER_WRITE_STATUS_ABORT;
  }

  if (header.bits_per_sample != data.bps) {
    data.error_msg = "ERROR: Samples in the frame uses unepected bit depth.";
    return FLAC__STREAM_DECODER_WRITE_STATUS_ABORT;
  }

  if (std::all_of(buffer, buffer + header.channels,
                  [](auto buf) { return buf == NULL; })) {
    data.error_msg = "ERROR: buffer is NULL";
    return FLAC__STREAM_DECODER_WRITE_STATUS_ABORT;
  }

  if (data.bps <= 8)
    fill_numpy_array(py::cast<py::array_t<int8_t>>(data.samples), N, n0, buffer,
                     data.justify);
  else if (data.bps <= 16)
    fill_numpy_array(py::cast<py::array_t<int16_t>>(data.samples), N, n0,
                     buffer, data.justify);
  else if (data.bps <= 32)
    fill_numpy_array(py::cast<py::array_t<int32_t>>(data.samples), N, n0,
                     buffer, data.justify);

  return FLAC__STREAM_DECODER_WRITE_STATUS_CONTINUE;
}

void metadata_callback(const FLAC__StreamDecoder* decoder,
                       const FLAC__StreamMetadata* metadata,
                       void* client_data) {
  /* print some stats */
  if (metadata->type == FLAC__METADATA_TYPE_STREAMINFO) {
    ReaderData& data = *(ReaderData*)client_data;
    if (data.samples.ndim() == 2)
      throw std::runtime_error("ERROR: Multiple streaminfo metadata found.");

    auto total_samples = metadata->data.stream_info.total_samples;
    auto channels = metadata->data.stream_info.channels;
    auto bps = metadata->data.stream_info.bits_per_sample;

    int justify_by = 0;
    if (bps <= 8) {
      data.samples = py::array_t<int8_t>({total_samples, (uint64_t)channels});
      if (bps < 8)
        justify_by = 8 - bps;
    } else if (bps <= 16) {
      data.samples = py::array_t<int16_t>({total_samples, (uint64_t)channels});
      if (bps < 16)
        justify_by = 16 - bps;
    } else if (bps <= 32) {
      data.samples = py::array_t<int32_t>({total_samples, (uint64_t)channels});
      if (bps < 32)
        justify_by = 32 - bps;
    } else {
      throw std::runtime_error("Invalid bitdepth specified");
    }
    data.sample_rate = metadata->data.stream_info.sample_rate;
    data.total_samples = total_samples;
    data.channels = channels;
    data.bps = bps;

    if (justify_by)
      data.justify = [justify_by](const int32_t x) {
        return x * (1 << justify_by);
      };
    else
      data.justify = [](const int32_t x) { return x; };
  }
}

void error_callback(const FLAC__StreamDecoder* decoder,
                    FLAC__StreamDecoderErrorStatus status, void* client_data) {
  ((ReaderData*)client_data)->error_msg =
      FLAC__StreamDecoderErrorStatusString[status];
}
} // namespace

py::tuple read(std::string filename) {
  FLAC__StreamDecoder* decoder = 0;
  FLAC__StreamDecoderInitStatus init_status;
  std::exception_ptr eptr;
  ReaderData client_data = {};

  if ((decoder = FLAC__stream_decoder_new()) == NULL)
    throw std::runtime_error("ERROR: allocating decoder");

  try {
    FLAC__stream_decoder_set_md5_checking(decoder, true);

    init_status = FLAC__stream_decoder_init_file(
        decoder, filename.c_str(), write_callback, metadata_callback,
        error_callback, &client_data);
    if (init_status != FLAC__STREAM_DECODER_INIT_STATUS_OK)
      throw std::runtime_error(
          FLAC__StreamDecoderInitStatusString[init_status]);

    FLAC__stream_decoder_process_until_end_of_stream(decoder);
  } catch (...) {
    eptr = std::current_exception(); // capture
  }

  FLAC__stream_decoder_delete(decoder);

  if (eptr)
    std::rethrow_exception(eptr);
  else if (!client_data.error_msg.empty())
    throw std::runtime_error(client_data.error_msg);

  return py::make_tuple(client_data.sample_rate,
                        client_data.samples.shape(1) != 1
                            ? client_data.samples
                            : client_data.samples.squeeze());
}
} // namespace flacfile
