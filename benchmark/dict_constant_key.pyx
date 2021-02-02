# cython: infer_types=True
# cython: language_level=3str
from libc.stdint cimport int32_t
from cpython cimport PyObject

cdef extern from "Python.h":
    object _PyDict_GetItem_KnownHash(object self, object key, Py_hash_t o)
    void Py_INCREF(PyObject*)



def test(d_0_top):
    d_1_top = dict__getitem_1(d_0_top, 'constant-key')
    return d_1_top

cdef inline dict__getitem_1(d_0_top, s_0):
    # s_0 = 'a'
    cdef int32_t label = 1
    while True:
        if label == 1:
            label = 2
            continue
        elif label == 2:
            d_1_top = _PyDict_GetItem_KnownHash(d_0_top, 'constant-key', 1275226973511038342)
            Py_INCREF(<PyObject*>d_1_top)
            return d_1_top