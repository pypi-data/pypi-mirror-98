#include <pybind11/pybind11.h>

#include "flacfile.h"
#include "flacfile_docstrings.h"

using namespace pybind11::literals;

PYBIND11_MODULE(__native__, m) {
  // m.doc() = NONE FOR __NATIVE__ GIVEN IN THE PARENT PACKAGE (PYTHON);

  m.def("read", &flacfile::read, "filename"_a.none(false), READ_DOCSTRING);
  m.def("write", &flacfile::write, "filename"_a.none(false), "rate"_a,
        "data"_a.none(false), WRITE_DOCSTRING);
}
