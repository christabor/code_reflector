import unittest
import css_reflector


class SelectorOutputTestCase(unittest.TestCase):

    def _setup(self):
        self.ref = css_reflector.CSSReflector()
