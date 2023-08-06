# -*- coding: utf-8 -*-
u"""
flacfile: Read & Write from FLAC sound files
============================================

Contents
--------
flacfile is a Python package wrapping libFLAC library to read/write FLAC audio files.

Functions
---------

   read
   write

"""

# import everything from pybind11 module and expose it as the top-level package
# content
from flacfile.__native__ import *

__all__ = ["read", "write"]
