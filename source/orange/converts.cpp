#include "c2py.hpp"

#include "converts.hpp"

bool convertFromPython(PyObject *obj, bool &b)
{ b = PyObject_IsTrue(obj) ? true : false;
  return true;
}


PyObject *convertToPython(const bool &b)
{ return PyInt_FromLong(b ? 1 : 0); }



bool convertFromPython(PyObject *obj, int &i)
{ if (PyInt_Check(obj))
    i=(int)PyInt_AsLong(obj);
  else if (PyLong_Check(obj))
    i=(int)PyLong_AsLong(obj);
  else
    PYERROR(PyExc_TypeError, "invalid integer", false);

  return true;
}


PyObject *convertToPython(const int &i)
{ return PyInt_FromLong(i); }


string convertToString(const int &i)
{ char is[128];
  sprintf(is, "%d", i);
  return is; }



bool convertFromPython(PyObject *obj, long &i)
{ if (PyInt_Check(obj))
    i=(long)PyInt_AsLong(obj);
  else if (PyLong_Check(obj))
    i=(long)PyLong_AsLong(obj);
  else
    PYERROR(PyExc_TypeError, "invalid integer", false);

  return true;
}


PyObject *convertToPython(const long &i)
{ return PyInt_FromLong(i); }


string convertToString(const long &i)
{ char is[128];
  sprintf(is, "%d", int(i));
  return is; }


bool convertFromPython(PyObject *obj, unsigned char &i)
{ if (PyInt_Check(obj))
    i=(unsigned char)PyInt_AsLong(obj);
  else if (PyLong_Check(obj))
    i=(unsigned char)PyLong_AsLong(obj);
  else
    PYERROR(PyExc_TypeError, "invalid integer", false);

  return true;
}


PyObject *convertToPython(const unsigned char &i)
{ return PyInt_FromLong(i); }


string convertToString(const unsigned char &i)
{ char is[128];
  sprintf(is, "%d", i);
  return is; }


bool convertFromPython(PyObject *obj, float &i)
{ if (PyFloat_Check(obj))
    i=(float)PyFloat_AsDouble(obj);
  else if (PyInt_Check(obj))
    i=(float)PyFloat_AsDouble(obj);
  else PYERROR(PyExc_TypeError, "invalid number", false);

  return true;
}


PyObject *convertToPython(const float &i)
{ return PyFloat_FromDouble(i); }


string convertToString(const float &i)
{ char is[128];
  sprintf(is, "%f", i);
  return is; }


bool convertFromPython(PyObject *obj, pair<float, float> &i)
{ return PyArg_ParseTuple(obj, "ff", &i.first, &i.second) != 0; }


PyObject *convertToPython(const pair<float, float> &i)
{ return Py_BuildValue("ff", i.first, i.second); }


string convertToString(const pair<float, float> &i)
{ char is[128];
  sprintf(is, "(%5.3f, %5.3f)", i.first, i.second);
  return is; 
}


bool convertFromPython(PyObject *obj, string &str)
{ if (!PyString_Check(obj))
    PYERROR(PyExc_TypeError, "invalid string", false);
  str=PyString_AsString(obj);
  return true;
}


PyObject *convertToPython(const string &str)
{ return PyString_FromString(str.c_str()); }


string convertToString(const string &str)
{ return str; }


float PyNumber_AsFloat(PyObject *o)
{ PyObject *number=PyNumber_Float(o);
  float res=(float)PyFloat_AsDouble(number);
  Py_DECREF(number);
  return res;
}


