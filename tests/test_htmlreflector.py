import unittest
import html_reflector


class SelectorOutputTestCase(unittest.TestCase):

    def _setup(self):
        self.ref = html_reflector.HTMLReflector()

    def test_single_class(self):
        self._setup()
        res = self.ref.process_string('.foo {}').extract().make_html(
            save_as_string=True)
        self.assertEqual(res, '<div class="foo"></div>')

    def test_single_id(self):
        self._setup()
        res = self.ref.process_string('#foo {}').extract().make_html(
            save_as_string=True)
        self.assertEqual(res, '<div id="foo"></div>')

    def test_nested_id(self):
        self._setup()
        res = self.ref.process_string('#foo #bar #bim {}').extract().make_html(
            save_as_string=True)
        expected = ('<div id="foo"><div id="bar"><div id="bim">'
                    '</div></div></div>')
        self.assertEqual(res, expected)

    def test_nested_class(self):
        self._setup()
        res = self.ref.process_string('.foo .bar .bim {}').extract().make_html(
            save_as_string=True)
        expected = ('<div class="foo"><div class="bar"><div class="bim">'
                    '</div></div></div>')
        self.assertEqual(res, expected)

    def test_compound_class_id(self):
        self._setup()
        res = self.ref.process_string('.foo#bar {}').extract().make_html(
            save_as_string=True)
        expected = ('<div class="foo" id="bar"></div>')
        self.assertEqual(res, expected)

    def test_compound_id_class(self):
        self._setup()
        res = self.ref.process_string('#foo.bar {}').extract().make_html(
            save_as_string=True)
        expected = ('<div class="foo" id="bar"></div>')
        self.assertEqual(res, expected)

    def test_nested_simple_class(self):
        self._setup()
        res = self.ref.process_string('.foo>.bar {}').extract().make_html(
            save_as_string=True)
        expected = ('<div class="foo"><div class="bar"></div></div>')
        self.assertEqual(res, expected)

    def test_nested_simple_id(self):
        self._setup()
        res = self.ref.process_string('#foo>#bar {}').extract().make_html(
            save_as_string=True)
        expected = ('<div id="foo"><div id="bar"></div></div>')
        self.assertEqual(res, expected)

    def test_nested_simple_id_spaces(self):
        self._setup()
        res = self.ref.process_string('#foo > #bar {}').extract().make_html(
            save_as_string=True)
        expected = ('<div id="foo"><div id="bar"></div></div>')
        self.assertEqual(res, expected)
