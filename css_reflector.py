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

    def _add_nested(self, k, el):
        """Parse nested element by its children."""
        el = Pq(el)
        tagname = Pq(el)[0].tag
        if tagname in self.invalid_tags:
            return
        selector = ''
        id, classes = el.attr('id'), el.attr('class')
        id = '#{}'.format(id) if id is not None else ''
        classes = '.{}'.format(classes) if classes is not None else ''
        if not id and not classes:
            selector = el[0].tag
        selector += '{}{}'.format(id, classes)
        children = Pq(el).children()
        if self._is_root_body_node(el):
            # Add for single nodes only
            if not children:
                self.selectors.add(selector)
            # Build nested css by traversing all child nodes and getting
            # their attributes.
            while children:
                for child in children:
                    child = Pq(child)
                    id, classes = child.attr('id'), child.attr('class')
                    # Order is important here. Id comes first, then classes,
                    # and classes must not have a space at the beginning,
                    # but must have one at the end, so that nested elements
                    # are properly represented, as well as selector chains.
                    if id is not None:
                        selector += ' #{}'.format(id)
                    if classes is not None:
                        classes = '.'.join(classes.split(' '))
                        selector += '.{} '.format(classes)
                    # Update child
                    children = Pq(child).children()
                    # Add selector on each loop, to show
                    # all variations of nesting in the css.
                    self.selectors.add(selector)
                    # Break on the first loop, since we replace children
                    # in the while loop above,
                    # thus preventing duplicate selectors.
                    break

    def _add(self, k, el):
        """Parse element, without considering children."""
        el = Pq(el)
        id, classes = el.attr('id'), el.attr('class')
        if id is not None:
            self.selectors['ids'].add(id)
        if classes is not None:
            for _class in classes.split(' '):
                self.selectors['classes'].add(_class.strip())

    def make_stylesheet(self, output=None, save_as_string=False):
        """Generate stylesheet string."""
        out = ''
        if self.nested:
            for sel in self.selectors:
                out += '{} '.format(sel) + '{}'
                if self.newlines_and_spaces:
                    out += '\n'
        else:
            for id in self.selectors['ids']:
                out += '#{} '.format(id.strip()) + '{}'
                if self.newlines_and_spaces:
                    out += '\n'
            for _class in self.selectors['classes']:
                out += '.{} '.format(_class.strip()) + '{}'
                if self.newlines_and_spaces:
                    out += '\n'
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
