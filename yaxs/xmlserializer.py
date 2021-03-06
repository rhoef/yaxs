"""
xmlserializer.py

Serialize and deserialize python objects to xml. Currently this works only for
objects that take no arguments in its __init__ method.

>>>class PyObj(XmlSerializer):
>>>    def __init__(self):
>>>        self.number = 42

pyobj = PyObj()
>>>string = pyobj.serialize()
>>>pyobj2 = XmlSerializer.deserialize(string)
>>>pyobj2.number
>>>42
>>>pyobj == pyobj2
>>>True

Any attribute that is in the pyobj.__dict__ is serialized. The values can be
any python atom and objects that are serializable i.e. subclasses of
XmlSerializer.

The attribute names are used as xml tag names and must fullfill the
following naming rules:

-) names can contain letters, numbers, and other characters
-) names cannot start with a number or punctuation character
-) names cannot start with the letters xml (or XML, or Xml, etc)
-) names cannot contain spaces

Dictionary keys must also follow these rules.
The method XmlSerializer._validate uses the following regex to test any
tag name to be xml conform, although the regex is a bit more restrictive

 '^(?!xml)[A-Za-z_][A-Za-z0-9._:]*$'

Only basestrings as type of dictionary keys are allowed.
"""

__author__ = 'rudolf.hoefler@gmail.com'
__licence__ = 'LGPL'


__all__ = ('XmlSerializer', )


import re
import numpy as np

from lxml import etree
from collections import OrderedDict


types = {float: float.__name__,
         int: int.__name__,
         long: long.__name__,
         str: str.__name__,
         unicode: unicode.__name__,
         complex: complex.__name__,
         unicode: unicode.__name__,
         list: list.__name__,
         tuple: tuple.__name__,
         dict: dict.__name__,
         OrderedDict: OrderedDict.__name__,
         bool: bool.__name__,
         None: type(None).__name__,
         set: set.__name__,
         frozenset: frozenset.__name__}

keytypes = ('str', 'unicode', 'int', 'long', 'float')


def key2tag(key):
    return "key_%s" %key

def tag2key(tag, keytype=None):
    tag = tag[4:]
    if keytype is None:
        return tag
    elif keytype in keytypes:
        return eval(keytype)(tag)
    else:
        raise TypeError('%s-type is not allowed as dict key' %keytype)


class XmlMetaSerializer(type):
    """Metaclass to 'register' all derived child classes."""

    def __init__(cls, name, bases, dct):

        if len(cls.__mro__) == 2:
            setattr(cls , "_classes", {})
        elif len(cls.__mro__)  >= 3:
            bases[0]._classes[name] = cls
            return type.__init__(cls, name, bases, dct)


class XmlSerializer(object):
    """Parenet for all serializable objects"""

    __metaclass__ = XmlMetaSerializer
    _type = 'type'
    _keytype = 'keytype'
    _subtype = 'subtype'

    def __init__(self, *args, **kw):
        super(XmlSerializer, self).__init__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def _validate(self, name):

        if not isinstance(name, basestring):
            raise TypeError('tag names must be string not %s' %type(name))

        if re.match('^(?!xml)[A-Za-z_][A-Za-z0-9._:]*$', name) is None:
            raise ValueError('%s is not a valid xml name' %name)

    def _from_value(self, value):

        if isinstance(value, bool):
            # booleans to lower case to be xml conform
            return str(value).lower()
        else:
            return str(value)

    def _from_seq(self, sequence):
        if isinstance(sequence, (set, frozenset)):
            stype = type(list(sequence)[0]).__name__
        else:
            stype = type(sequence[0]).__name__
        txt = " ".join([str(item) for item in sequence])
        return txt, stype

    def _is_seq(self, value):
        return isinstance(value, (list, tuple, set, frozenset))

    def _dict2etree(self, tag, dict_, keytype=None):

        element = etree.Element(tag)
        element.attrib[self._type] = type(dict_).__name__

        if keytype is None:
            element.attrib[self._keytype] = type(tag).__name__
        else:
            element.attrib[self._keytype] = keytype

        for key_, value in dict_.iteritems():
            key =  key2tag(key_)
            self._validate(key)
            if isinstance(value, dict):
                element.append(
                    self._dict2etree(key, value, type(key_).__name__))
            elif self._is_seq(value):
                child = etree.SubElement(element, key)
                child.attrib[self._type] = type(value).__name__
                child.attrib[self._keytype] = type(key_).__name__
                text, stype = self._from_seq(value)
                child.text = text
                child.attrib[self._subtype] = stype
            else:
                child = etree.SubElement(element, key)
                child.attrib[self._type] = type(value).__name__
                child.attrib[self._keytype] = type(key_).__name__
                child.text = self._from_value(value)

        return element

    def to_xml(self, name=None):
        if name is None:
            name = self.__class__.__name__

        root = etree.Element(name)
        root.attrib[self._type] = type(self).__name__

        for key, value in self.__dict__.iteritems():
            self._validate(key)

            if isinstance(value, dict):
                root.append(self._dict2etree(key, value))
            elif value.__class__.__name__ in self._classes:
                root.append(value.to_xml(key))
            elif self._is_seq(value):
                child = etree.SubElement(root, key)
                child.attrib[self._type] = type(value).__name__
                text, stype = self._from_seq(value)
                child.text = text
                child.attrib[self._subtype] = stype
            else:
                child = etree.SubElement(root, key)
                child.attrib[self._type] = type(value).__name__
                child.text = self._from_value(value)

        return root

    def serialize(self, pretty_print=True):
        root = self.to_xml()
        return etree.tostring(root, pretty_print=pretty_print)

    @classmethod
    def deserialize(cls, string):
        root = etree.fromstring(string)
        obj = cls._classes[root.tag]()
        obj.load(string)
        return obj

    def load(self, root):
        if isinstance(root, basestring):
            root = etree.fromstring(root)

        for child in root.getchildren():
            self.__dict__[child.tag] = self._to_attr(child)

    def _to_seq(self, element):
        try:
            stype = eval(element.attrib[self._subtype])
            return [stype(item) for item in element.text.split()]
        except NameError:
            # in case of e.g float64 or float32
            stype = element.attrib[self._subtype]
            return [np.asscalar(np.array([v], dtype=stype))
                    for v in element.text.split()]

    def _to_attr(self, element):
        _type = element.attrib[self._type]

        if _type in (types[int], types[float], types[long], types[complex]):
            return eval(element.text)
        elif _type == types[bool]:
            return eval(element.text.title())
        elif _type in (types[str], types[unicode]):
            return element.text
        elif _type == types[list]:
            return self._to_seq(element)
        elif _type == types[tuple]:
            return tuple(self._to_seq(element))
        elif _type == types[set]:
            return set(self._to_seq(element))
        elif _type == types[frozenset]:
            return frozenset(self._to_seq(element))
        elif _type in (types[dict], types[OrderedDict]):
            return self._etree2dict(element)
        elif _type in self._classes:
            inst = self._classes[_type]()
            inst.load(element)
            return inst
        elif _type == types[None]:
            return None
        else:
            raise RuntimeError('cannot deserialize %s' %_type)

    def _etree2dict(self, element):
        edict = {}
        for child in element.getchildren():
            edict[tag2key(child.tag,  child.attrib[self._keytype])] = \
                self._to_attr(child)

        return edict
