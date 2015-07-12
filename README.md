# codeReflector
A suite of tools to parse and transform web formats, for web applications and automation.

## Components

### CSS Reflector

Takes HTML and converts it to corresponding CSS. Though, it doesn't truly "convert". It parses the HTML and extracts the ids and classes, outputting them to blank selectors.

Example:

```html
<div id="foo"></div><div class="bar bim"></div>
... it becomes
#foo {} .bar {} .bim {}
or, with nested=True set, and
<div id="foo">
    <div id="bar">
        <div id="bam" class="foo foo2"></div>
    </div>
</div>
...it becomes
#foo #bar #bam.foo.foo2 {}
```

### HTML Reflector

Takes CSS and converts it to corresponding HTML. Similar to Emmett, but fully OSS, and programmable (and handles spaces for nested selectors). Also designed to work in conjunction with other **Reflector** modules.

Example:

```html
.foo#bar -> <div class="foo" id="bar"></div>
```

## Tests

Test coverage provided by nose. Run tests via ```python nosetests tests/```
