from tinycss import make_parser
from pyquery import PyQuery as Pq
from pprint import pprint as ppr
from reflector import Reflector
from string import ascii_lowercase

DEBUG = __name__ == '__main__'

"""
        NOTE!
        NOTE!
        WORK IN PROGRESS -- NOT COMPLETE OR FULLY WORKING!!!!

"""


class HTMLReflector(Reflector):

    def __init__(self, default_tag='div'):
        self.selectors = set()
        self.parser = make_parser('page3')
        self.default_tag = default_tag
        self.css = None

    def process_string(self, css_string):
        """Parse stylesheet with tinycss."""
        self.css = self.parser.parse_stylesheet_bytes(css_string)
        return self

    def process(self, filename):
        """Parse stylesheet file with tinycss."""
        self.css = self.parser.parse_stylesheet_file(filename)
        return self

    def extract(self):
        """Extracts css document into a dictionary grouped
        by ids and classes for later use. CSS nesting and relationships
        remain intact."""
        for rule in self.css.rules:
            try:
                sels = rule.selector.as_css().split(',')
                for sel in set(sels):
                    self.selectors.add(sel)
            except AttributeError:
                print('Error: Selector `{}` is not valid'.format(sel))
                continue
        return self

    def _get_id(self, piece):
        """Get the id of the piece, if it's at the beginning,
        or somewhere in between."""
        if '#' in piece:
            if piece.startswith('#'):
                return ' id="{}"'.format(piece.replace('#', ''))
            else:
                pos = piece.find('#') + 1
                return ' id="{}"'.format(piece[pos:])
        else:
            return ''

    def _get_class(self, piece):
        """Get the class of the piece, if it's at the beginning,
        or somewhere in between."""
        if '.' in piece:
            if piece.startswith('.'):
                return ' class="{}"'.format(piece.replace('.', ''))
            else:
                pos = piece.find('.') + 1
                return ' class="{}"'.format(piece[pos:])
        else:
            return ''

    def _is_tag(self, piece):
        """Check if it's an actual html, e.g. `div`, `em`"""
        return piece[0] in ascii_lowercase

    def _get_tag(self, piece):
        """Return the html tag if it has no id/class selectors,
        otherwise, get the substring that only contains the html tag."""
        if self._is_tag(piece):
            pos = piece.find('#')
            if pos == -1:
                pos = piece.find('.')
                if pos == -1:
                    return piece
            return piece[:pos]
        else:
            return self.default_tag

    def _create_tag(self, selector):
        #   1. .foo.bar
        #   2. #foo#bar
        #   3. div.foo
        #   4. div.foo#bar, div#foo.bar
        #   5. div+#foo.bar
        #   6. .foo>.bar > div#bam div.foo

        html = ''
        pieces = [x.strip() for x in selector.split('>')]
        if len(pieces) == 1:
            pieces = [x.strip() for x in selector.split(' ')]
        print(pieces)

        for k, piece in enumerate(pieces):
            tag = self._get_tag(piece)
            id = self._get_id(piece)
            classes = self._get_class(piece)
            space = k * (' ' * 4)
            html += '{space}<{tag}{id}{classes}>\n'.format(
                piece, space=space, id=id, classes=classes, tag=tag)
        # To build the nested html, we need to loop over them in reverse,
        # to make sure we get the corresponding selector/html tag
        for k, piece in enumerate(reversed(pieces)):
            tag = self._get_tag(piece) if self._is_tag(piece) \
                else self.default_tag
            space = k * (' ' * 4)
            html += '</{tag}>\n'.format(space=space, tag=tag)
        return html

    def make_html(self, output=None, save_as_string=False):
        """Build out and write the actual HTML document."""
        if save_as_string:
            out = ''
            for selector in self.selectors:
                out += self._create_tag(selector)
            return out
        if not output.endswith('.html'):
            raise ValueError('{} if is not a valid html file.'.format(output))
        with open(output, 'wb+') as newfile:
            for selector in self.selectors:
                newfile.write(self._create_tag(selector))
        return self

if DEBUG:
    hreflector = HTMLReflector()
    hreflector.process('test.css').extract().make_html(output='output.html')
