# -*- coding: utf-8 -*-

__author__ = """Chris Tabor (dxdstudio@gmail.com)"""

from pyquery import PyQuery as Pq
from reflector import Reflector
from pprint import pprint as ppr

DEBUG = __name__ == '__main__'


class CSSReflector(Reflector):

    invalid_tags = ['body', 'head', 'title', 'meta']

    def __init__(self, nested=True, newlines_and_spaces=False):
        self.newlines_and_spaces = newlines_and_spaces
        self.nested = nested
        if nested:
            self.selectors = set()
        else:
            self.selectors = {'classes': set(), 'ids': set()}

    def __str__(self):
        ppr(self.selectors)
        return ''

    def _is_root_body_node(self, element):
        """Determine if element is a direct child of <html> or <body>,
        and thus a 'root' element (outside of html)"""
        parent = Pq(element).parent()[0].tag
        return parent in ['body', 'html']

    def _format_classes(self, classes, spaces=''):
        if classes is None:
            return ''
        _classes = ''
        for _class in classes.split(' '):
            _classes += '{spaces}.{}'.format(_class.strip(), spaces=spaces)
        return '{}'.format(_classes)

    def _format_id(self, id):
        return '#{}'.format(id) if id is not None else ''

    def _format_selector(self, el, id, classes):
        selector = ''
        if not id and not classes:
            selector = el[0].tag
        selector += '{}{}'.format(id, classes)
        return selector

    def _add_nested(self, k, el):
        """Parse nested element by its children."""
        el = Pq(el)
        tagname = Pq(el)[0].tag
        if tagname in self.invalid_tags:
            return
        id = self._format_id(el.attr('id'))
        classes = self._format_classes(el.attr('class'))
        selector = self._format_selector(el, id, classes)
        children = Pq(el).children()
        if not self._is_root_body_node(el):
            return
        # Add for single nodes only
        if not children:
            self.selectors.add(selector)
        # Build nested css by traversing all child nodes and getting
        # their attributes.
        while children:
            for child in children:
                # 1. Add current
                self.selectors.add(selector)
                # 2. Add child
                child = Pq(child)
                child = Pq(child)
                selector += self._add_id_and_classes(child)
                self.selectors.add(selector)
                # # 3. Move to next children
                children = child.children()

    def _add_id_and_classes(self, node):
        """Order is important here. Id comes first, then classes,
        and classes must not have a space at the beginning,
        but must have one at the end, so that nested elements
        are properly represented, as well as selector chains."""
        id, classes = node.attr('id'), node.attr('class')
        extra = ''
        if id is not None:
            extra += ' #{}'.format(id)
        if classes is not None:
            classes = '.'.join(classes.split(' '))
            spaces = '' if id is not None and len(classes) > 1 else ' '
            extra += self._format_classes(classes, spaces=spaces)
        return extra

    def _add(self, k, el):
        """Parse element, without considering children."""
        el = Pq(el)
        id, classes = el.attr('id'), el.attr('class')
        if id is not None:
            self.selectors['ids'].add(id)
        if classes is not None:
            for _class in classes.split(' '):
                self.selectors['classes'].add(_class.strip())

    def _format_selectors(self, selectors):
        out = ''
        for sel in sorted(selectors):
            out += '{} '.format(sel) + '{}'
            if self.newlines_and_spaces:
                out += '\n'
        return out

    def _format_stylesheet(self):
        """Format the output for writing to file or string.
        Styles can be divided as shallow, separate lists of ids and classes,
        or compound, nested CSS (typical)."""
        out = ''
        if self.nested:
            out += self._format_selectors(self.selectors)
        else:
            out += self._format_selectors(self.selectors['ids'])
            out += self._format_selectors(self.selectors['classes'])
        return out

    def make_stylesheet(self, output=None, save_as_string=False):
        """Generate stylesheet string."""
        out = self._format_stylesheet()
        if save_as_string:
            return out
        self._write(output, out)

    def _write(self, output, out):
        if not output.endswith('.css'):
            raise ValueError('{} if is not a valid css file.'.format(output))
        with open(output, 'wb+') as newfile:
            newfile.write(out)

    def _process(self):
        if self.nested:
            self.doc.find('*').each(self._add_nested)
        else:
            self.doc.find('*').each(self._add)

    def process_string(self, html_string):
        """Parse html with pyquery."""
        self.doc = Pq(html_string)
        self._process()
        return self

    def process(self, filename):
        with open(filename) as _file:
            self.doc = Pq(_file.read())
        self._process()
        return self


if DEBUG:
    hreflector = CSSReflector(newlines_and_spaces=True)
    hreflector.process('test.html').make_stylesheet('output-test.css')
