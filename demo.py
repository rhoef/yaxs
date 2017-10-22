"""
demo.py
"""

__author__ = 'rudolf.hoefler@gmail.com'
__copyright__ = 'LGPL'


import sys
from yaxs import XmlSerializer
from lxml import etree

class Testi(XmlSerializer):

    def __init__(self, *args, **kw):
        super(Testi, self).__init__(*args, **kw)
        self.dict = {'foo': 'bar'}


class Test(XmlSerializer):

    def __init__(self):
        super(Test, self).__init__()

        self.boolean = True
        self.none = None
        self.foo = 3.14
        self.n = 42
        self.set = set([1,2,3])
        self.frozenset = frozenset([1,2,4])
        self.liste = [1, 3, 5]
        self.tuple = (1, 2, 3)
        self.bar = {'foo': 'bar',
                    'bar': 'baz',
                    '0037': '0037',
                    'baz': {'fooobar':1}}
        self.inst = Testi()


test = Test()
print test.serialize()
test2 = XmlSerializer.deserialize(test.serialize())

import pdb; pdb.set_trace()
