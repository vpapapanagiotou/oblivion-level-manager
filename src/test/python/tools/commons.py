from unittest import TestCase

from tools.formatting import BColors


class BColorsTest(TestCase):
    def test1(self):
        print(BColors.HEADER.value + "Header" + BColors.ENDC.value)
        print(BColors.OKBLUE.value + "Ok Blue" + BColors.ENDC.value)
        print(BColors.OKCYAN.value + "Ok Cyan" + BColors.ENDC.value)
        print(BColors.OKGREEN.value + "Ok Green" + BColors.ENDC.value)
        print(BColors.WARNING.value + "Warning" + BColors.ENDC.value)
        print(BColors.FAIL.value + "Fail" + BColors.ENDC.value)
        print(BColors.BOLD.value + "Bold" + BColors.ENDC.value)
        print(BColors.ITALIC.value + "Italic" + BColors.ENDC.value)
        print(BColors.UNDERLINE.value + "Underline" + BColors.ENDC.value)
