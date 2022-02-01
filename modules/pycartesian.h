/* --------------------------------------------------------------------
Copyright (C) 2009 Swedish Meteorological and Hydrological Institute, SMHI,

This file is part of RAVE.

RAVE is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RAVE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with RAVE.  If not, see <http://www.gnu.org/licenses/>.
------------------------------------------------------------------------*/
/**
 * Python version of the Cartesian API.
 * @file
 * @author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
 * @date 2009-12-10
 */
#ifndef PYCARTESIAN_H
#define PYCARTESIAN_H
#include "cartesian.h"

/**
 * A cartesian product
 */
typedef struct {
  PyObject_HEAD /*Always has to be on top*/
  Cartesian_t* cartesian; /**< the cartesian product */
} PyCartesian;

#define PyCartesian_Type_NUM 0                       /**< index of type */

#define PyCartesian_GetNative_NUM 1                  /**< index of GetNative */
#define PyCartesian_GetNative_RETURN Cartesian_t*    /**< return type for GetNative */
#define PyCartesian_GetNative_PROTO (PyCartesian*)   /**< arguments for GetNative */

#define PyCartesian_New_NUM 2                        /**< index of New */
#define PyCartesian_New_RETURN PyCartesian*          /**< return type for New */
#define PyCartesian_New_PROTO (Cartesian_t*)         /**< arguments for New */

#define PyCartesian_API_pointers 3                   /**< number of api pointers */

#define PyCartesian_CAPSULE_NAME "_cartesian._C_API"

#ifdef PYCARTESIAN_MODULE
/** Forward declaration of type*/
extern PyTypeObject PyCartesian_Type;

/** Checks if the object is a PyCartesian or not */
#define PyCartesian_Check(op) ((op)->ob_type == &PyCartesian_Type)

/** Forward declaration of PyCartesian_GetNative */
static PyCartesian_GetNative_RETURN PyCartesian_GetNative PyCartesian_GetNative_PROTO;

/** Forward declaration of PyCartesian_New */
static PyCartesian_New_RETURN PyCartesian_New PyCartesian_New_PROTO;

#else
/** pointers to types and functions */
static void **PyCartesian_API;

/**
 * Returns a pointer to the internal cartesian, remember to release the reference
 * when done with the object. (RAVE_OBJECT_RELEASE).
 */
#define PyCartesian_GetNative \
  (*(PyCartesian_GetNative_RETURN (*)PyCartesian_GetNative_PROTO) PyCartesian_API[PyCartesian_GetNative_NUM])

/**
 * Creates a new cartesian instance. Release this object with Py_DECREF. If a Cartesian_t instance is
 * provided and this instance already is bound to a python instance, this instance will be increfed and
 * returned.
 * @param[in] cartesian - the Cartesian_t intance.
 * @returns the PyCartesian instance.
 */
#define PyCartesian_New \
  (*(PyCartesian_New_RETURN (*)PyCartesian_New_PROTO) PyCartesian_API[PyCartesian_New_NUM])

/**
 * Checks if the object is a python cartesian.
 */
#define PyCartesian_Check(op) \
   (Py_TYPE(op) == &PyCartesian_Type)

#define PyCartesian_Type (*(PyTypeObject*)PyCartesian_API[PyCartesian_Type_NUM])

/**
 * Imports the PyArea module (like import _area in python).
 */
#define import_pycartesian() \
    PyCartesian_API = (void **)PyCapsule_Import(PyCartesian_CAPSULE_NAME, 1);

#ifdef KALLE

/**
 * Checks if the object is a python cartesian.
 */
#define PyCartesian_Check(op) \
   ((op)->ob_type == (PyTypeObject *)PyCartesian_API[PyCartesian_Type_NUM])

/**
 * Imports the PyCartesian module (like import _polarscan in python).
 */
static int
import_pycartesian(void)
{
  PyObject *module;
  PyObject *c_api_object;

  module = PyImport_ImportModule("_cartesian");
  if (module == NULL) {
    return -1;
  }

  c_api_object = PyObject_GetAttrString(module, "_C_API");
  if (c_api_object == NULL) {
    Py_DECREF(module);
    return -1;
  }
#if PY_MAJOR_VERSION < 3
  PyCartesian_API = (void **)PyCObject_AsVoidPtr(c_api_object);
#else
  PyCartesian_API = (void **)PyCapsule_New((void *)c_api_object, NULL, NULL);
#endif
/*
  if (PyCObject_Check(c_api_object)) {
    PyCartesian_API = (void **)PyCObject_AsVoidPtr(c_api_object);
  }
*/
  Py_DECREF(c_api_object);
  Py_DECREF(module);
  return 0;
}
#endif


#endif

#endif /* PYCARTESIAN_H */
