#pragma once

constexpr auto READ_DOCSTRING = R"(Open a FLAC file.

Return the sample rate (in samples/sec) and data from a FLAC file.

Parameters
----------
filename : string or open file handle
    Input FLAC file.

Returns
-------
rate : int
    Sample rate of FLAC file.

data : numpy array
    Data read from FLAC file. Data-type is determined from bits_per_sample info;
    see Notes. Data is 1-D for 1-channel FLAC, or 2-D of shape 
    (Nsamples, Nchannels) otherwise.

Notes
-----
Common data types:
=====================  ===========  ===========  =============
        FLAC format            Min          Max    NumPy dtype
=====================  ===========  ===========  =============
32-bit integer PCM     -2147483648  +2147483647  int32
24-bit integer PCM     -2147483648  +2147483392  int32
16-bit integer PCM     -32768       +32767       int16
8-bit integer PCM      -128         +127         int8
=====================  ===========  ===========  =============

FLAC supports from 4 to 32 bits per sample. Data is returned in the smallest
compatible numpy int type, in left-justified format. For example, 24-bit data
will be stored as int32, with the MSB of the 24-bit data stored at the MSB of
the int32, and typically the least significant byte is 0x00.

References
----------
.. [1] Xiph.Org Foundation, \"FLAC format\" https://xiph.org/flac/format.html

Examples
--------
>>> import flacfile
>>>
>>> import matplotlib.pyplot as plt
>>> import numpy as np

Assume your flac file "myaudio.flac" is located in the current working directory

>>> flac_fname = "myaudio.flac"

Load the .flac file contents then print number of channels & the total duration.

>>> samplerate, data = flacfile.read(flac_fname)
>>> print(f\"number of channels = {data.shape[1]}\")
>>> length = data.shape[0] / samplerate
>>> print(f\"length = {length}s\")

Plot the waveform assuming stereo.

>>> time = np.linspace(0., length, data.shape[0])
>>> plt.plot(time, data[:, 0], label=\"Left channel\")
>>> plt.plot(time, data[:, 1], label=\"Right channel\")
>>> plt.legend()
>>> plt.xlabel(\"Time [s]\")
>>> plt.ylabel(\"Amplitude\")
>>> plt.show()
)";

constexpr auto WRITE_DOCSTRING = R"(Write a NumPy array as a FLAC file.

Parameters
----------
filename : string or open file handle
    Output flac file.
rate : int
    The sample rate (in samples/sec).
data : ndarray
    A 1-D or 2-D NumPy array of integer data-type.

Notes
-----
* Writes a flac file with medium compression.
* To write multiple-channels, use a 2-D array of shape (Nsamples, Nchannels).
* The bits-per-sample will be determined by the data-type. Note the maximum bps
  setting of the libFLAC encoder is 24 bits. If data array is in int32, the most
  significant 24 bits are encoded and the least significant 8 bits are ignored.

Common data types:
  =============  =====================  ===========  ===========
  NumPy dtype    flac bits-per-sample   Min          Max        
  =============  =====================  ===========  ===========
  int32          24-bit                 -2147483648  +2147483647
  int16          16-bit                 -32768       +32767     
  int8           8-bit                  -128         +127       
  =============  =====================  ===========  ===========

References
----------
.. [1] Xiph.Org Foundation, \"FLAC format\" https://xiph.org/flac/format.html

Examples
--------
Create a 100Hz sine wave, sampled at 44100Hz. Write to 16-bit PCM, Mono.

>>> from flacfile import write
>>> samplerate = 44100; fs = 100
>>> t = np.linspace(0., 1., samplerate)
>>> amplitude = np.iinfo(np.int16).min
>>> data = amplitude * np.sin(2. * np.pi * fs * t)
>>> write("example.flac", samplerate, data.astype(np.int16)))";
