# codeReflector
A suite of tools to parse and transform web formats, for web applications and automation.

## Components

### CSS Reflector

Takes HTML and converts it to corresponding CSS. Though, it doesn't truly "convert". It parses the HTML and extracts the ids and classes, outputting them to blank selectors.

Example:

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

Takes CSS and converts it to corresponding HTML. Similar to Emmett, but fully OSS, and programmable (and handles spaces for nested selectors). Also designed to work in conjunction with other **Reflector** modules.

Example:

```css
.foo.bar#bar
```
becomes
```html
<div class="foo bar" id="bar"></div>
```

## Tests

Test coverage provided by nose. Run tests via ```python nosetests tests/```
