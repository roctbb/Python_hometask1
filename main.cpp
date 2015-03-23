#include <stdio.h>

extern "C" {
#include <Python.h>
}

static PyObject * calculate(PyObject *module, PyObject *args)
{
	PyObject * M = PyTuple_GetItem(args, 0);
	int size = PyObject_Size(M);
	double ** mas = (double**)malloc(size * sizeof(double*));
	for (int i = 0; i < size; ++i)
	{
		mas[i] = (double*)malloc(size * sizeof(double));
		PyObject * row = PyList_GetItem(M, i);
		for (int j = 0; j < size; ++j)
		{
			PyObject * element = PyList_GetItem(row, j);
			mas[i][j] = PyFloat_AsDouble(element);
		}
	}
	for (int k = 0; k < size; ++k)
		for (int i = 0; i < size; ++i)
			for (int j = 0; j < size; ++j)
				mas[i][j] = 1.0 / ( 1.0 / mas[i][j] + 1.0 / (mas[i][k] + mas[k][j]) );
	for (int i = 0; i < size; ++i)
	{
		PyObject * row = PyList_GetItem(M, i);
		for (int j = 0; j < size; ++j)
		{
			PyObject * value = PyFloat_FromDouble(mas[i][j]);
			PyList_SetItem(row, j, value);
		}
	}
	for (int i = 0; i < size; ++i) free(mas[i]);
	free(mas);
	Py_INCREF(Py_None);
	return Py_None;
}

PyMODINIT_FUNC PyInit_resistance()
{
	static PyMethodDef ModuleMethods[] = {
		{ "calculate", calculate, METH_VARARGS,
				"Arguments:\n"
				"a square matrix"
		},
		{ NULL, NULL, 0, NULL }
	};
	static PyModuleDef ModuleDef = {
		PyModuleDef_HEAD_INIT,
		"resistance",
		"Resistance calculation.",
		-1, ModuleMethods, 
		NULL, NULL, NULL, NULL
	};
	PyObject * module = PyModule_Create(&ModuleDef);
	return module;
}
