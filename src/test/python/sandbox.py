from unittest import TestCase

from tools.common import print_exception


class Sandbox(TestCase):
    def test1(self):
        try:
            assert False
        except AssertionError as e:
            e.args += ("hello!",)
            raise
