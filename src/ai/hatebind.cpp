#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // vector用
#include "hate.cpp"

namespace py = pybind11;
PYBIND11_MODULE(hate, m)
{
    m.doc() = "hate made by pybind11";
    // py::class_<Piece>(m, "Blocks")
    //     .def(py::init())
    //     .def("print_piece", &Piece::print);
    py::class_<Hatetris>(m, "Hate")
        .def(py::init<std::vector<std::vector<int>> &>())
        .def("get_first_piece", &Hatetris::getFirstPiece)
        .def("get_next_piece", &Hatetris::getHatetris)
        .def("print", &Hatetris::print);
}
