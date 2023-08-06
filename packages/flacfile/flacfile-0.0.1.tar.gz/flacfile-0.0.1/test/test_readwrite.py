import flacfile

import numpy as np


def test_write_read(flac_filename, samples, ch, dtype, fs):
    x = samples(dtype, fs, ch)

    flacfile.write(flac_filename, fs, x)
    fs1, x1 = flacfile.read(flac_filename)

    assert fs == fs1
    assert x1.ndim == (2 if ch > 1 else 1)

    if ch>1:
        print(x[:10,0])
        print(x1[:10,0])
    assert np.array_equal(x, x1)


def pytest_generate_tests(metafunc):
    if "ch" in metafunc.fixturenames:
        metafunc.parametrize("ch", range(1, 9))
    if "dtype" in metafunc.fixturenames:
        metafunc.parametrize("dtype", (np.int8, np.int16, np.int32))

