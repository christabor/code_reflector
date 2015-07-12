from tinycss import make_parser
from pprint import pprint as ppr
from reflector import Reflector
from string import ascii_lowercase

DEBUG = __name__ == '__main__'


class HTMLReflector(Reflector):

    def __init__(self, default_tag='div', newlines_and_spaces=False):
        self.selectors = set()
        self.parser = make_parser('page3')
        self.newlines_and_spaces = newlines_and_spaces
        self.default_tag = default_tag
        self.css = None

    def __str__(self):
        ppr(self.selectors)
        return ''

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
                piece = piece[1:]
            # If this is a chained selector, stop before the next token
            end = piece.find('.') if piece.find('.') != -1 else len(piece)
            return ' id="{}"'.format(piece[:end].replace('#', ' '))
        else:
            return ''

    def _get_class(self, piece):
        """Get the class of the piece, if it's at the beginning,
        or somewhere in between."""
        if '.' in piece:
            if piece.startswith('.'):
                piece = piece[1:]
            # If this is a chained selector, stop before the next token
            end = piece.find('#') if piece.find('#') != -1 else len(piece)
            return ' class="{}"'.format(piece[:end].replace('.', ' '))
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

    def _get_attributes(self, piece):
        if '#' in piece and not piece.startswith('#'):
            start = piece.find('#')
            id = self._get_id(piece[start:])
            classes = self._get_class(piece)
        elif '.' in piece and not piece.startswith('.'):
            id = self._get_id(piece)
            start = piece.find('.')
            classes = self._get_class(piece[start:])
        else:
            id = self._get_id(piece)
            classes = self._get_class(piece)
        tag = self._get_tag(piece)
        return tag, id, classes

    def _get_pieces(self, selector):
        pieces = [x.strip() for x in selector.split('>')]
        for k, piece in enumerate(pieces):
            if ' ' in piece:
                for token in reversed(piece.split(' ')):
                    pieces.insert(k, token)
                pieces.remove(piece)
        return pieces

    def _create_tag(self, selector):
        html = ''
        pieces = self._get_pieces(selector)
        for k, piece in enumerate(pieces):
            tag, id, classes = self._get_attributes(piece)
            space = k * (' ' * 4) if self.newlines_and_spaces else ''
            html += '{space}<{tag}{id}{classes}>'.format(
                piece, space=space, id=id, classes=classes, tag=tag)
            if self.newlines_and_spaces:
                html += '\n'
        # To build the nested html, we need to loop over them in reverse,
        # to make sure we get the corresponding selector/html tag
        _k = len(pieces)
        for piece in reversed(pieces):
            tag = self._get_tag(piece) if self._is_tag(piece) \
                else self.default_tag
            space = _k * (' ' * 4) if self.newlines_and_spaces else ''
            html += '{space}</{tag}>'.format(space=space, tag=tag)
            if self.newlines_and_spaces:
                html += '\n'
            _k -= 1
        return html

    def make_html(self, output=None, save_as_string=False):
        """Build out and write the actual HTML document."""
        out = ''
        for selector in self.selectors:
            out += self._create_tag(selector)
        if save_as_string:
            return out
        if not output.endswith('.html'):
            raise ValueError('{} if is not a valid html file.'.format(output))
        with open(output, 'wb+') as newfile:
            newfile.write(out)
        return self

if DEBUG:
    hreflector = HTMLReflector(newlines_and_spaces=True)
    hreflector.process('test.css').extract().make_html(output='output.html')
