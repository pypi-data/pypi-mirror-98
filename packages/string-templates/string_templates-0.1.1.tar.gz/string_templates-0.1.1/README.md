# string_templates

Library to create string templates in python and execute them.

## Single line

```python
render("Hello, $name", name="Tom")
# "Hello, Tom"
```
    

## Multiline strings

```python
render("""
Hello
$name
""", name="Tom")
# '\nHello\nTom\n'

# no newline at start and end
render("""\
Hello
$name\
""", name="Tom")
# 'Hello\nTom'
```

## template classes

```python
@template
class Test:
    name: str
    _template = """Hello, $name"""
str(Test("Tom"))
# 'Hello, Tom'
```
