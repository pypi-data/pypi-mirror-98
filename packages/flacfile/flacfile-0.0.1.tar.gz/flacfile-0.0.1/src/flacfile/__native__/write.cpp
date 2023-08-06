#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include <FLAC/stream_encoder.h>
// #include <FLAC/metadata.h>

#include <fmt/format.h>
using namespace fmt::literals;

#include "flacfile.h"

namespace py = pybind11;

namespace flacfile {

namespace {

#define READSIZE 1024

void progress_callback(const FLAC__StreamEncoder* encoder,
                       FLAC__uint64 bytes_written, FLAC__uint64 samples_written,
                       unsigned frames_written, unsigned total_frames_estimate,
                       void* client_data) {
  // possible TODO: call Python callback function
  // fprintf(stderr,
  //         "wrote %" PRIu64 " bytes, %" PRIu64 "/%u samples, %u/%u frames\n",
  //         bytes_written, samples_written, total_samples, frames_written,
  //         total_frames_estimate);
}

template <class T>
bool write_data(FLAC__StreamEncoder* encoder, py::array_t<T> data,
                const int justify_by) {
  bool ok = true;
  auto r = data.unchecked();
  bool mch = r.ndim() > 1; // true if multi-channel
  uint32_t channels = mch ? (uint32_t)r.shape(1) : 1;
  uint32_t left = mch ? (uint32_t)r.shape(0) : (uint32_t)r.size();
  uint32_t total_samples = 0;
  constexpr uint32_t TOTAL_BUF_SIZE = 1024 * 1024 / 4;
  FLAC__int32 buf[TOTAL_BUF_SIZE]; // work with total buffer size of 512 kB
  FLAC__int32* pcm[FLAC__MAX_CHANNELS];

  // samples are interpreted as fixed-point values. If numpy byte size is
  // greater than the flac bps, take the most-significant bps bits.
  std::function<int32_t(const int32_t)> justify;
  if (justify_by)
    justify = [justify_by](const int32_t x) { return x / (1 << justify_by); };
  else
    justify = [](const int32_t x) { return x; };

  // create per-channel PCM buffers
  size_t nbuf = TOTAL_BUF_SIZE / channels;
  for (uint32_t i = 0; i < channels; ++i)
    pcm[i] = buf + i * nbuf;

  size_t n0 = 0;
  if (mch) {
    while (ok && left) {
      uint32_t need = (left > READSIZE ? (size_t)READSIZE : (size_t)left);
      for (uint32_t j = 0; j < channels; ++j) // channels
      {
        for (uint32_t i = 0; i < need; ++i) // samples
        {
          pcm[j][i] = justify(r(i + n0, j));
        }
      }
      ok = FLAC__stream_encoder_process(encoder, pcm, need);
      n0 += need;
      left -= need;
    }
  } else {
    while (ok && left) {
      uint32_t need = (left > READSIZE ? (size_t)READSIZE : (size_t)left);
      for (uint32_t i = 0; i < need; ++i) // samples
      {
        pcm[0][i] = justify(r(i + n0));
      }
      ok = FLAC__stream_encoder_process(encoder, pcm, need);
      n0 += need;
      left -= need;
    }
  }
  return ok;
}

} // namespace

/**
 * write data to flac file
 *
 * TODOs
 * []- add metadata option
 * []- add bps option
 * []- add verify option
 * []- add compression_level option
 * []- add progress_cb option
 **/
void write(std::string filename, unsigned sample_rate, py::array data) {

  FLAC__StreamEncoder* encoder = 0;
  FLAC__StreamEncoderInitStatus init_status;
  // FLAC__StreamMetadata *metadata[2];
  // FLAC__StreamMetadata_VorbisComment_Entry entry;

  std::exception_ptr eptr;

  /* validate ndarray size */
  auto ndim = data.ndim();
  auto ncols = ndim > 1 ? data.shape(0) : data.size();
  auto nrows = ndim > 1 ? data.shape(1) : 1;
  auto dtype = data.dtype();

  if (ndim < 1 || ndim > 2)
    throw std::invalid_argument("Data must be 1D or 2D array");

  if (!nrows || nrows > FLAC__MAX_CHANNELS)
    throw std::invalid_argument(
        "Too many audio channels. Number of rows of data must be non-zero and less than or equal to {}"_format(
            FLAC__MAX_CHANNELS));

  if (!sample_rate || sample_rate > FLAC__MAX_SAMPLE_RATE)
    throw std::invalid_argument(
        "Out-of-range sample_rate: must be non-zero and less than or equal to {}"_format(
            FLAC__MAX_SAMPLE_RATE));

  auto nbytes = dtype.itemsize();
  if (dtype.kind() != 'i' && (nbytes == 8 || nbytes == 16 || nbytes == 32))
    throw std::invalid_argument("Unsupported data type: data.dtype must be "
                                "'int8', 'int16', or 'int32'.");

  /* set  */
  FLAC__bool verify = true;
  uint32_t channels = (uint32_t)nrows;
  uint32_t bps = 8 * (uint32_t)nbytes;
  FLAC__uint64 total_samples = (FLAC__uint64)ncols;
  uint32_t compression_level = 5;

  /* libFLAC encoder limitation */
  if (bps > 24)
    bps = 24;

  /* allocate the encoder */
  if ((encoder = FLAC__stream_encoder_new()) == NULL)
    throw std::runtime_error("ERROR: allocating encoder");

  try {
    if (!FLAC__stream_encoder_set_verify(encoder, verify))
      throw std::runtime_error("FLAC Encoder failed to verify.");

    if (!FLAC__stream_encoder_set_compression_level(encoder, compression_level))
      throw std::runtime_error("FLAC failed to set the compression level.");

    if (!FLAC__stream_encoder_set_channels(encoder, channels))
      throw std::runtime_error("FLAC failed to set the number of channels.");

    if (!FLAC__stream_encoder_set_bits_per_sample(encoder, bps))
      throw std::runtime_error("FLAC failed to set bits-per-sample.");

    if (!FLAC__stream_encoder_set_sample_rate(encoder, sample_rate))
      throw std::runtime_error("FLAC failed to set sample rate.");

    if (!FLAC__stream_encoder_set_total_samples_estimate(encoder,
                                                         total_samples))
      throw std::runtime_error("FLAC failed to set total samples estimate.");

    /* now add some metadata; we'll add some tags and a padding block */
    // if(ok) {
    // 	if(
    // 		(metadata[0] =
    // FLAC__metadata_object_new(FLAC__METADATA_TYPE_VORBIS_COMMENT)) == NULL ||
    // 		(metadata[1] =
    // FLAC__metadata_object_new(FLAC__METADATA_TYPE_PADDING))
    // == NULL ||
    // 		/* there are many tag (vorbiscomment) functions but these are
    // convenient for this particular use: */
    // 		!FLAC__metadata_object_vorbiscomment_entry_from_name_value_pair(&entry,
    // "ARTIST", "Some Artist") ||
    // 		!FLAC__metadata_object_vorbiscomment_append_comment(metadata[0],
    // entry,
    // /*copy=*/false) || /* copy=false: let metadata object take control of
    // entry's allocated string */
    // 		!FLAC__metadata_object_vorbiscomment_entry_from_name_value_pair(&entry,
    // "YEAR", "1984") ||
    // 		!FLAC__metadata_object_vorbiscomment_append_comment(metadata[0],
    // entry,
    // /*copy=*/false) 	) { 		fprintf(stderr, "ERROR: out of memory or
    // tag error\n"); 		ok = false;
    // 	}

    // 	metadata[1]->length = 1234; /* set the padding length */

    // 	ok = FLAC__stream_encoder_set_metadata(encoder, metadata, 2);
    // }

    /* initialize encoder */
    init_status = FLAC__stream_encoder_init_file(
        encoder, filename.c_str(), progress_callback, /*client_data=*/nullptr);
    if (init_status != FLAC__STREAM_ENCODER_INIT_STATUS_OK)
      throw std::runtime_error(
          FLAC__StreamEncoderInitStatusString[init_status]);

    /* read blocks of samples from WAVE file and feed to encoder */

    bool ok = false;
    if (bps <= 8)
      ok = write_data(encoder, py::cast<py::array_t<int8_t>>(data), 8 - bps);
    else if (bps <= 16)
      ok = write_data(encoder, py::cast<py::array_t<int16_t>>(data), 16 - bps);
    else // if (bps <= 32)
      ok = write_data(encoder, py::cast<py::array_t<int32_t>>(data), 32 - bps);
    if (!ok)
      throw std::runtime_error("Encoding failed: {}"_format(
          FLAC__StreamEncoderStateString[FLAC__stream_encoder_get_state(
              encoder)]));

    if (!FLAC__stream_encoder_finish(encoder))
      throw std::runtime_error("FLAC Encoder failed to close the stream.");

    /* now that encoding is finished, the metadata can be freed */
    // FLAC__metadata_object_delete(metadata[0]);
    // FLAC__metadata_object_delete(metadata[1]);
  } catch (...) {
    eptr = std::current_exception(); // capture
  }

  FLAC__stream_encoder_delete(encoder);

  if (eptr)
    std::rethrow_exception(eptr);
}
} // namespace flacfile
