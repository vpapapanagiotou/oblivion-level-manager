from unittest import TestCase

from tools.common import print_exception


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
