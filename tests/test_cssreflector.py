# -*- coding: utf-8 -*-

__author__ = """Chris Tabor (dxdstudio@gmail.com)"""

import unittest
import css_reflector


class SelectorOutputTestCase(unittest.TestCase):

    def _setup(self):
        self.ref = css_reflector.CSSReflector()
