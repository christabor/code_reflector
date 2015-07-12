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
        self.assertEqual(res, '#foo #bar #bim {}#foo #bar {}#foo {}')

    def test_nested_class(self):
        self._setup()
        res = self.ref.process_string(self._wrap(
            '<div class="foo"><div class="bar"><div class="bim">'
            '</div></div></div>')).make_stylesheet(
                save_as_string=True)
        self.assertEqual(res, '.foo {}.foo .bar .bim {}.foo .bar {}')

    def test_compound_class_id(self):
        self._setup()
        res = self.ref.process_string(self._wrap(
            '<div id="bar" class="foo"></div>')).make_stylesheet(
                save_as_string=True)
        self.assertEqual(res, '#bar.foo {}')

    def test_compound_multiclass(self):
        self._setup()
        res = self.ref.process_string(self._wrap(
            '<div class="foo bar bim"></div>')).make_stylesheet(
                save_as_string=True)
        self.assertEqual(res, '.foo.bar.bim {}')

    def test_compound_id_multiclass(self):
        self._setup()
        res = self.ref.process_string(self._wrap(
            '<div id="foo" class="bar bim bam"></div>')).make_stylesheet(
                save_as_string=True)
        self.assertEqual(res, '#foo.bar.bim.bam {}')

    def test_nested_multiid_multiclass_tag(self):
        self._setup()
        html = """
        <div class="foo">
            <div class="bar">
            <section id="bam">
                <section class="quux"></section>
            </section>
            </div>
        </div>
        """
        expected = ('.foo {}'
                    '.foo .bar #bam .quux {}'
                    '.foo .bar #bam {}'
                    '.foo .bar {}'
                    ).replace('\n', '')
        res = self.ref.process_string(self._wrap(html)).make_stylesheet(
            save_as_string=True)
        self.assertEqual(res, expected)
