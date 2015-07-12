import unittest
import html_reflector


class SelectorOutputTestCase(unittest.TestCase):

    def _setup(self):
        self.ref = html_reflector.HTMLReflector()

    def test_single_class(self):
        self._setup()
        res = self.ref.process_string('.foo {}').extract().make_html(
            save_as_string=True)
        self.assertEqual(res, '<div class="foo">\n</div>\n')

    def test_single_id(self):
        self._setup()
        res = self.ref.process_string('#foo {}').extract().make_html(
            save_as_string=True)
        self.assertEqual(res, '<div id="foo">\n</div>\n')
