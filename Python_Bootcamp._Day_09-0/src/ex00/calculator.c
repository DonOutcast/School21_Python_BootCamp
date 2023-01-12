#define PY_SSIZE_T_CLEAN
#include <Python.h>

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }
int divide(int a, int b) { return (int)(a / b); }

double fadd(double a, double b) { return a + b; }
double fsub(double a, double b) { return a - b; }
double fmul(double a, double b) { return a * b; }
double fdivide(double a, double b) { return a / b; }

static PyObject *_add(PyObject *self, PyObject *args) {
    const int *obj1;
    const int *obj2;
    if (PyTuple_Size(args) != 2) {
        PyErr_SetString(self, "Must have 2 arguments");
    }
    if (!PyArg_ParseTuple(args, "OO", &obj1, &obj2)) {
          Py_INCREF(Py_None);
          return Py_None;
    }
    if ((PyFloat_Check(obj1)) && (PyFloat_Check(obj2))) {
        double res;
        double _a, _b;
        _a = PyFloat_AsDouble(obj1);
        _b = PyFloat_AsDouble(obj2);
        res = fadd(_a, _b);
        return PyFloat_FromDouble(res);
    } else if ((PyLong_Check(obj1)) && (PyLong_Check(obj2))) {
        int res;
        int _a, _b;
        _a = PyLong_AsLong(obj1);
        _b = PyLong_AsLong(obj2);
        res = add(_a, _b);
        return PyLong_FromLong(res);
    } else {
        PyErr_SetString(PyExc_TypeError,
                        "Both argument must be Double or Integer");
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *_sub(PyObject *self, PyObject *args) {
    const int *obj1;
    const int *obj2;
    if (PyTuple_Size(args) != 2) {
        PyErr_SetString(self, "Must have 2 arguments");
    }
    if (!PyArg_ParseTuple(args, "OO", &obj1, &obj2)) {
          Py_INCREF(Py_None);
          return Py_None;
    }
    if ((PyFloat_Check(obj1)) && (PyFloat_Check(obj2))) {
        double res;
        double _a, _b;
        _a = PyFloat_AsDouble(obj1);
        _b = PyFloat_AsDouble(obj2);
        res = fsub(_a, _b);
        return PyFloat_FromDouble(res);
    } else if ((PyLong_Check(obj1)) && (PyLong_Check(obj2))) {
        int res;
        int _a, _b;
        _a = PyLong_AsLong(obj1);
        _b = PyLong_AsLong(obj2);
        res = sub(_a, _b);
        return PyLong_FromLong(res);
    } else {
        PyErr_SetString(PyExc_TypeError,
                        "Both argument must be Double or Integer");
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *_mul(PyObject *self, PyObject *args) {
    const int *obj1;
    const int *obj2;
    if (PyTuple_Size(args) != 2) {
        PyErr_SetString(self, "Must have 2 arguments");
    }
    if (!PyArg_ParseTuple(args, "OO", &obj1, &obj2)) {
          Py_INCREF(Py_None);
          return Py_None;
    }
    if ((PyFloat_Check(obj1)) && (PyFloat_Check(obj2))) {
        double res;
        double _a, _b;
        _a = PyFloat_AsDouble(obj1);
        _b = PyFloat_AsDouble(obj2);
        res = fmul(_a, _b);
        return PyFloat_FromDouble(res);
    } else if ((PyLong_Check(obj1)) && (PyLong_Check(obj2))) {
        int res;
        int _a, _b;
        _a = PyLong_AsLong(obj1);
        _b = PyLong_AsLong(obj2);
        res = mul(_a, _b);
        return PyLong_FromLong(res);
    } else {
        PyErr_SetString(PyExc_TypeError,
                        "Both argument must be Double or Integer");
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *_divide(PyObject *self, PyObject *args) {
    const int *obj1;
    const int *obj2;
    if (PyTuple_Size(args) != 2) {
        PyErr_SetString(self, "Must have 2 arguments");
    }
    if (!PyArg_ParseTuple(args, "OO", &obj1, &obj2)) {
          Py_INCREF(Py_None);
          return Py_None;
    }
    if ((PyFloat_Check(obj1)) && (PyFloat_Check(obj2))) {
        double res;
        double _a, _b;
        _a = PyFloat_AsDouble(obj1);
        _b = PyFloat_AsDouble(obj2);
        if (_b == 0) {
            PyErr_SetString(PyExc_ZeroDivisionError, "Cannot divide by zero");
              Py_INCREF(Py_None);
              return Py_None;
        }
        res = fdivide(_a, _b);
        return PyFloat_FromDouble(res);
    } else if ((PyLong_Check(obj1)) && (PyLong_Check(obj2))) {
        int res;
        int _a, _b;
        _a = PyLong_AsLong(obj1);
        _b = PyLong_AsLong(obj2);
        if (_b == 0) {
            PyErr_SetString(PyExc_ZeroDivisionError, "Cannot divide by zero");
                Py_INCREF(Py_None);
                return Py_None;
        }
        res = divide(_a, _b);
        return PyLong_FromLong(res);
    } else {
        PyErr_SetString(PyExc_TypeError,
                        "Both argument must be Double or Integer");
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef ModuleMethods[] = {{"add", _add, METH_VARARGS, ""},
                                      {"sub", _sub, METH_VARARGS, ""},
                                      {"mul", _mul, METH_VARARGS, ""},
                                      {"div", _divide, METH_VARARGS, ""},
                                      {NULL, NULL, 0, NULL}};

static struct PyModuleDef calculator = {PyModuleDef_HEAD_INIT, "calculator",
                                        NULL, -1, ModuleMethods};

PyMODINIT_FUNC PyInit_calculator(void) { return PyModule_Create(&calculator); }