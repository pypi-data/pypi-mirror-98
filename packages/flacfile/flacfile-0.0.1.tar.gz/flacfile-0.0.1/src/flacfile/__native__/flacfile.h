#pragma once

#include <string>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace flacfile {
pybind11::tuple read(std::string filename);
void write(std::string filename, unsigned sample_rate, pybind11::array data);
}
