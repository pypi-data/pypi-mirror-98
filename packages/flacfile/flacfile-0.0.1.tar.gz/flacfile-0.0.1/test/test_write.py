import pytest

import flacfile

import numpy as np


def test_invalid_writes(flac_filename, samples):
    fs = 8000
    ch = 2
    dtype = np.int16
    x = samples(dtype, fs, ch)

    # cannot be None
    with pytest.raises(TypeError):
        flacfile.write(None, fs, x)

    # must be str
    with pytest.raises(TypeError):
        flacfile.write(0, fs, x)

    # cannot be None
    with pytest.raises(TypeError):
        flacfile.write(flac_filename, None, x)

    # must be unsigned int
    with pytest.raises(TypeError):
        flacfile.write(flac_filename, -1, x)

    # cannot be None
    with pytest.raises(TypeError):
        flacfile.write(flac_filename, fs, None)

    # must be np.ndarray
    with pytest.raises(TypeError):
        flacfile.write(flac_filename, fs, [0])

    # invalid file name
    with pytest.raises(RuntimeError):
        flacfile.write("", fs, x)

    # out-of-range fs
    with pytest.raises(ValueError):
        flacfile.write(flac_filename, 100000000, x)

    # need at least 1 channel
    with pytest.raises(ValueError):
        flacfile.write(flac_filename, fs, samples(dtype, fs, 0))

    # too many channels
    with pytest.raises(ValueError):
        flacfile.write(flac_filename, fs, samples(dtype, fs, 10))

    # ok datatype (internally casted)
    flacfile.write(flac_filename, fs, samples(np.int64, fs, ch))

    # invalid datatype
    with pytest.raises(ValueError):
        flacfile.write(flac_filename, fs, samples(dtype, fs, ch).astype(float))
