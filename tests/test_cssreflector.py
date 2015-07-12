# -*- coding: utf-8 -*-

__author__ = """Chris Tabor (dxdstudio@gmail.com)"""

import unittest
import css_reflector


class SelectorOutputTestCase(unittest.TestCase):

    def _setup(self):
        self.ref = css_reflector.CSSReflector()

    def _wrap(self, html):
        return '<html><body>{}</body></html>'.format(html)

    def test_single_class(self):
        self._setup()
        res = self.ref.process_string(self._wrap(
            '<div class="foo"></div>')).make_stylesheet(
                save_as_string=True)
        self.assertEqual(res, '.foo {}')

    def test_single_id(self):
        self._setup()
        res = self.ref.process_string(self._wrap(
            '<div id="foo"></div>')).make_stylesheet(
                save_as_string=True)
        self.assertEqual(res, '#foo {}')

    def test_nested_id(self):
        self._setup()
        res = self.ref.process_string(self._wrap(
            '<div id="foo"><div id="bar"><div id="bim">'
            '</div></div></div>')).make_stylesheet(
                save_as_string=True)
        self.assertEqual(res, '#foo #bar #bim {}#foo #bar {}')
