"""
test.py

Unit tests for the xmls package

"""

__author__ = 'rudolf.hoefler@gmail.com'
__copyright__ = 'LGPL'

__all__ = ('TestSerialisation', )

import unittest
from xmls import XmlSerializer


class TestTypes(unittest.TestCase):

    @staticmethod
    def serialize_deserialize(pyobj, Class):
        string = pyobj.serialize()
        pyobj2 = Class()
        pyobj2.deserialize(string)
        return pyobj2

    def test_boolean(self):

        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = True

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))

    def test_int(self):

        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = 42

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))

    def test_float(self):

        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = True

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))

    def test_None(self):


        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = None

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))

    def test_set(self):

        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = set([1, 2, 3])

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))

    def test_frozenset(self):

        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = frozenset([1, 2, 3])

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))

    def test_tuple(self):

        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = tuple([1, 2, 3])

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))

    def test_list(self):

        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = list([1, 2 ,3])

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))

    def test_dict(self):

        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = {'integer': 1,
                              'float': 3.14,
                              'dictionary': {'number': 1}}

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))


    def test_pyobject(self):

        class SubPyObj(XmlSerializer):

            def __init__(self, *args, **kw):
                super(SubPyObj, self).__init__(*args, **kw)
                self.value = 42

        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = SubPyObj()

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))


    def test_complex(self):

        class PyObj(XmlSerializer):
            def __init__(self, *args, **kw):
                super(PyObj, self).__init__(*args, **kw)
                self.value = 1*1.5j

        pyobj = PyObj()
        self.assertEqual(pyobj, self.serialize_deserialize(pyobj, PyObj))


if __name__ == '__main__':
    unittest.main()
