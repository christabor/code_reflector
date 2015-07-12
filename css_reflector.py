from pyquery import PyQuery as Pq
from reflector import Reflector
from pprint import pprint as ppr

DEBUG = __name__ == '__main__'


class CSSReflector(Reflector):

    def __init__(self, filename):
        self.selectors = {'classes': set(), 'ids': set()}
        with open(filename) as _file:
            self.doc = Pq(_file.read())

    def __str__(self):
        ppr(self.selectors)
        return ''

    def _print(self, k, el):
        el = Pq(el)
        id, classes = el.attr('id'), el.attr('class')
        if id is not None:
            self.selectors['ids'].add(id)
        if classes is not None:
            for _class in classes.split(' '):
                self.selectors['classes'].add(_class.strip())

    def make_stylesheet(self, output):
        if not output.endswith('.css'):
            raise ValueError('{} if is not a valid css file.'.format(output))
        with open(output, 'wb+') as newfile:
            for id in self.selectors['ids']:
                newfile.write('#{} '.format(id) + '{}\n')
            for _class in self.selectors['classes']:
                newfile.write('.{} '.format(_class) + '{}\n')

    def process(self):
        self.doc.find('*').each(self._print)
        return self


if DEBUG:
    hreflector = CSSReflector('test.html')
    hreflector.process()
    hreflector.make_stylesheet('output-test.css')
    # print(hreflector)
