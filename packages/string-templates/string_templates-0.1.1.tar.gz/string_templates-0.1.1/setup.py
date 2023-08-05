# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['string_templates']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'string-templates',
    'version': '0.1.1',
    'description': 'simple string template library',
    'long_description': '# string_templates\n\nLibrary to create string templates in python and execute them.\n\n## Single line\n\n```python\nrender("Hello, $name", name="Tom")\n# "Hello, Tom"\n```\n    \n\n## Multiline strings\n\n```python\nrender("""\nHello\n$name\n""", name="Tom")\n# \'\\nHello\\nTom\\n\'\n\n# no newline at start and end\nrender("""\\\nHello\n$name\\\n""", name="Tom")\n# \'Hello\\nTom\'\n```\n\n## template classes\n\n```python\n@template\nclass Test:\n    name: str\n    _template = """Hello, $name"""\nstr(Test("Tom"))\n# \'Hello, Tom\'\n```\n',
    'author': 'JulianSobott',
    'author_email': 'julian.sobott@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JulianSobott/string_templates',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
