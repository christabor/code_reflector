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
        self.assertEqual(res, '#foo {}#foo #bar {}#foo #bar #bim {}')

    def test_nested_class(self):
        self._setup()
        res = self.ref.process_string(self._wrap(
            '<div class="foo"><div class="bar"><div class="bim">'
            '</div></div></div>')).make_stylesheet(
                save_as_string=True)
        self.assertEqual(res, '.foo {}.foo .bar {}.foo .bar .bim {}')

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
        expected = (
            '.foo {}'
            '.foo .bar {}'
            '.foo .bar #bam {}'
            '.foo .bar #bam .quux {}'
        ).replace('\n', '')
        res = self.ref.process_string(self._wrap(html)).make_stylesheet(
            save_as_string=True)
        self.assertEqual(res, expected)

    def test_nested_allmulti_complex(self):
        html = """
        <div class="foo" id="foo">
            <div class="bar" id="boom">
                <div class="quux">
                    <div class="nested nested2" id="foo3"></div>
                </div>
                <div class="baz"></div>
            </div>
        </div>
        """
        expected = (
            '#foo.foo {}'
            '#foo.foo #boom.bar {}'
            '#foo.foo #boom.bar .quux {}'
            '#foo.foo #boom.bar .quux .baz {}'
            '#foo.foo #boom.bar .quux #foo3.nested.nested2 {}'
        ).replace('\n', '')
        self._setup()
        res = self.ref.process_string(self._wrap(html)).make_stylesheet(
            save_as_string=True)
        self.assertEqual(res, expected)

    def test_nested_deeply_nested(self):
        html = """
        <div class="foo0">
            <div class="foo1">
                <div class="foo2">
                    <div class="foo3">
                        <div class="foo4">
                            <div class="foo5"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        expected = (
            '.foo0 {}'
            '.foo0 .foo1 {}'
            '.foo0 .foo1 .foo2 {}'
            '.foo0 .foo1 .foo2 .foo3 {}'
            '.foo0 .foo1 .foo2 .foo3 .foo4 {}'
            '.foo0 .foo1 .foo2 .foo3 .foo4 .foo5 {}'
        ).replace('\n', '')
        self._setup()
        res = self.ref.process_string(self._wrap(html)).make_stylesheet(
            save_as_string=True)
        self.assertEqual(res, expected)

    def test_nested_deeply_nested_multiclass(self):
        html = """
        <div class="foo0">
            <div class="foo1 foo_1">
                <div class="foo2">
                    <div class="foo3">
                        <div class="foo4">
                            <div class="foo5 foo_5"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        expected = (
            '.foo0 {}'
            '.foo0 .foo1.foo_1 {}'
            '.foo0 .foo1.foo_1 .foo2 {}'
            '.foo0 .foo1.foo_1 .foo2 .foo3 {}'
            '.foo0 .foo1.foo_1 .foo2 .foo3 .foo4 {}'
            '.foo0 .foo1.foo_1 .foo2 .foo3 .foo4 .foo5.foo_5 {}'
        ).replace('\n', '')
        self._setup()
        res = self.ref.process_string(self._wrap(html)).make_stylesheet(
            save_as_string=True)
        self.assertEqual(res, expected)
