[![Build Status](https://travis-ci.org/christabor/codeReflector.svg?branch=master)](https://travis-ci.org/christabor/codeReflector)
[![MIT Badge](http://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/christabor/codeReflector/master/LICENSE)

# codeReflector
A suite of tools to parse and transform web formats, for web applications and automation.

## Components

### CSS Reflector

Takes HTML and converts it to corresponding CSS. Though, it doesn't truly "convert". It parses the HTML and extracts the ids and classes, outputting them to blank selectors.

Example:

Using
```python
css_reflector = CSSReflector(newlines_and_spaces=True)
hreflector.process('myhtmlfile.html').make_stylesheet(output='output.css')
```

```html
<div id="foo">
    <div id="bar">
        <div id="bam" class="foo foo2"></div>
    </div>
</div>
```
becomes
```css
#foo {}
#foo #bar {}
#foo #bar #bam.foo.foo2 {}
```
or, if nested is set to False,
```css
#foo #bar #bam.foo.foo2 {}
```

### HTML Reflector

Takes CSS and converts it to corresponding HTML. Similar to Emmett, but fully OSS, and programmable (and handles spaces for nested selectors). Also designed to work in conjunction with other **Reflector** components.

Example:

Using
```python
htmlreflector = HTMLReflector(newlines_and_spaces=True)
htmlreflector.process('mycssfile.css').extract().make_html(output='output.html')
```

```css
.foo.bar#bar
```
becomes
```html
<div class="foo bar" id="bar"></div>
```

## Requirements

See [requirements.txt](requirements.txt) for more.

## Installation
```python
python setup.py install
```

## Tests

Test coverage provided by nose. Run tests via ```python nosetests tests/```
