from typing import List
from unittest import TestCase

from character import Attribute


class Sandbox(TestCase):
    def test1(self):
        try:
            assert False
        except AssertionError as e:
            e.args += ("hello!",)
            raise

    def test2(self):
        x = ['abc', 'def', 'ghi']
        print('abc' in x)

    def test3(self):
        a = set()
        a.add(Attribute("blade"))
        a.add(Attribute("blunt"))
        a.add(Attribute("blade"))
        print(a)
