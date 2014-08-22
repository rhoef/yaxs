yaxs
====

Yet another xml serializer. 

Yaxs is not really a serious project since there are already a plenty of serializers 
out there (and much more sophisticated ones). 
One goal was to have a human readable output which can be easily reverse engineered the others.

Currently, yaxs works only for objects that take no arguments in its ```__init__``` method. 
It is implemented as factory pattern, where each subclass of ```XmlSerializer`` is a product. 

How it works:
-------------

```
class PyObj(XmlSerializer):
    def __init__(self):
        self.number = 42

pyobj = PyObj()
string = pyobj.serialize()
pyobj2 = XmlSerializer.deserialize(string)
pyobj2.number
42
pyobj == pyobj2
True
```

Any attribute that is in the ```pyobj.__dict__``` is serialized. The values can be
any python atom and objects that are serializable i.e. subclasses of
XmlSerializer.

The attribute names are used as xml tag names and must fullfill the
following naming rules:

-  names can contain letters, numbers, and other characters
-  names cannot start with a number or punctuation character
-  names cannot start with the letters xml (or XML, or Xml, etc)
-  names cannot contain spaces

Dictionary keys must also follow these rules.
The method XmlSerializer._validate uses the following regex to test any
tag name to be xml conform, although the regex is a bit more restrictive
```
 '^(?!xml)[A-Za-z_][A-Za-z0-9._:]*$'
```
Only basestrings as type of dictionary keys are allowed.

Tests
-----
```python tests/test.py```
