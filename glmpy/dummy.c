#include <Python.h>

static PyModuleDef dummy_module = {
    PyModuleDef_HEAD_INIT,
    "dummy",
    NULL,
    -1,
    NULL
};

PyMODINIT_FUNC PyInit_dummy(void) {
    return PyModule_Create(&dummy_module);
}