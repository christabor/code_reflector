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

    def test_nested_multiadjacent(self):
        html = """
        <div class="foo"></div>
        <div class="bar">
            <div class="foo"></div>
        </div>
        <div class="baz"></div>
        """
        expected = (
            '.bar {}'
            '.bar .foo {}'
            '.baz {}'
            '.foo {}'
        ).replace('\n', '')
        self._setup()
        res = self.ref.process_string(self._wrap(html)).make_stylesheet(
            save_as_string=True)
        self.assertEqual(res, expected)

    def test_nested_multiadjacent_composite(self):
        html = """
        <div class="foo" id="foo"></div>
        <div class="bar" id="bar">
            <div class="foo"></div>
        </div>
        <div class="baz" id="baz"></div>
        """
        expected = (
            '#bar.bar {}'
            '#bar.bar .foo {}'
            '#baz.baz {}'
            '#foo.foo {}'
        ).replace('\n', '')
        self._setup()
        res = self.ref.process_string(self._wrap(html)).make_stylesheet(
            save_as_string=True)
        self.assertEqual(res, expected)

    def test_nested_multiadjacent_composite_complex(self):
        html = """
        <div class="foo" id="foo"></div>
        <div class="bar" id="bar">
            <div class="foo">
                <div class="foo2">
                    <div class="foo3a foo3b foo3c" id="deepfoo"></div>
                </div>
            </div>
        </div>
        <div class="baz" id="baz">
            <div id="baz2" class="baz2"></div>
        </div>
        <div class="quux" id="quux">
            <div id="quux2" class="quux2"></div>
        </div>
        """
        expected = (
            '#bar.bar {}'
            '#bar.bar .foo {}'
            '#bar.bar .foo .foo2 {}'
            '#bar.bar .foo .foo2 #deepfoo.foo3a.foo3b.foo3c {}'
            '#baz.baz {}'
            '#baz.baz #baz2.baz2 {}'
            '#foo.foo {}'
            '#quux.quux {}'
            '#quux.quux #quux2.quux2 {}'
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
