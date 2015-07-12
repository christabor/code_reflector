# codeReflector
A suite of tools to parse and output different types of code for building web applications.

## This is a WIP - stay tuned for more.

## Components

### CSS Reflector

Takes HTML and converts it to corresponding CSS. Though, it doesn't truly "convert". It parses the HTML and extracts the ids and classes, outputting them to blank selectors.

Example:

```
<div id="foo"></div><div class="bar bim"></div>
#foo {} .bar {} .bim {}
```

### HTML Reflector

Takes CSS and converts it to corresponding HTML. Similar to Emmett, but fully OSS, and programmable. Also designed to work in conjunction with other **Reflector** modules.

Example:

```
.foo#bar -> <div class="foo" id="bar"></div>
```

## Tests

Test coverage provided by nose. Run tests via ```python nosetests tests/```
