# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_typing_only_imports']

package_data = \
{'': ['*']}

install_requires = \
['flake8']

entry_points = \
{'flake8.extension': ['TYO100 = flake8_typing_only_imports:Plugin']}

setup_kwargs = {
    'name': 'flake8-typing-only-imports',
    'version': '0.2.2',
    'description': 'A flake8 plugin to flag imports exclusively used for type annotations',
    'long_description': '<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://img.shields.io/pypi/v/flake8-typing-only-imports.svg" alt="Package version">\n</a>\n<a href="https://codecov.io/gh/sondrelg/flake8-typing-only-imports">\n    <img src="https://codecov.io/gh/sondrelg/flake8-typing-only-imports/branch/master/graph/badge.svg" alt="Code coverage">\n</a>\n<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://github.com/sondrelg/flake8-typing-only-imports/actions/workflows/testing.yml/badge.svg" alt="Test status">\n</a>\n<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Supported Python versions">\n</a>\n<a href="http://mypy-lang.org/">\n    <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">\n</a>\n\n# flake8-typing-only-imports\n\n> Plugin is still a work in progress\n\nTells you which imports to put inside type-checking blocks.\n\n## Codes\n\n| Code   | Description                                         |\n|--------|-----------------------------------------------------|\n| TYO100 | Move import into a type-checking block  |\n| TYO101 | Move third-party import into a type-checking block |\n| TYO102 | Found multiple type checking blocks |\n| TYO200 | Add \'from \\_\\_future\\_\\_ import annotations\' import |\n| TYO201 | Annotation does not need to be a string literal |\n| TYO300 | Annotation needs to be made into a string literal |\n| TYO301 | Annotation does not need to be a string literal |\n\n## Rationale\n\n`TYO100` guards\nagainst [import cycles](https://mypy.readthedocs.io/en/stable/runtime_troubles.html?highlight=TYPE_CHECKING#import-cycles)\n. `TYO101` applies the same logic, for `venv` or `stdlib` imports.\n\nRemaining error codes are there to help manage\n[forward references](https://mypy.readthedocs.io/en/stable/runtime_troubles.html?highlight=TYPE_CHECKING#class-name-forward-references),\neither by telling your to use string literals where needed, or by enabling\n[postponed evaluation of annotations](https://www.python.org/dev/peps/pep-0563/).\nThe error code series `TYO2XX` and `TYO3XX` should therefore be considered\nmutually exclusive, as they represent two different ways of managing forward\nreferences.\n\nSee [this](https://stackoverflow.com/a/55344418/8083459) excellent stackoverflow answer for a\nquick explanation of forward references.\n\n## Installation\n\n```shell\npip install flake8-typing-only-imports\n```\n\n## Suggested use\n\nOnly enable `TYO101` if you\'re after micro performance gains on start-up.\n\n`TYO2XX` and `TYO3XX` are reserved for error codes to help manage forward references.\nIt does not make sense to enable both series, and they should be considered mutually exclusive.\n\nIf you\'re adding this to your project, we would recommend something like this:\n\n```python\nselect = TYO100, TYO200, TYO200  # or TYO300 and TYO301\n\nignore = TYO101, TYO300, TYO301  # or TYO200 and TYO201\n```\n\n## Examples\n\n**Bad code**\n\n`models/a.py`\n```python\nfrom models.b import B\n\nclass A(Model):\n    def foo(self, b: B): ...\n```\n\n`models/b.py`\n```python\nfrom models.a import A\n\nclass B(Model):\n    def bar(self, a: A): ...\n```\n\nWhich will first result in these errors\n```shell\n>> a.py: TYO101: Move third-party import \'models.b.B\' into a type-checking block\n>> b.py: TYO101: Move third-party import \'models.a.A\' into a type-checking block\n```\n\nand consequently trigger these errors if imports are purely moved into type-checking block, without proper forward reference handling\n\n```shell\n>> a.py: TYO300: Annotation \'B\' needs to be made into a string literal\n>> b.py: TYO300: Annotation \'A\' needs to be made into a string literal\n```\n\n**Good code**\n\n`models/a.py`\n```python\nfrom typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n    from models.b import B\n\nclass A(Model):\n    def foo(self, b: \'B\'): ...\n```\n`models/b.py`\n```python\nfrom typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n    from models.a import A\n\nclass B(Model):\n    def bar(self, a: \'A\'): ...\n```\n\n## As a pre-commit hook\n\nYou can run this flake8 plugin as a [pre-commit](https://github.com/pre-commit/pre-commit) hook:\n\n```yaml\n- repo: https://gitlab.com/pycqa/flake8\n  rev: 3.7.8\n  hooks:\n    - id: flake8\n      additional_dependencies: [ flake8-typing-only-imports ]\n```\n\n## Supporting the project\n\nLeave a&nbsp;⭐️&nbsp; if this project helped you!\n\nContributions are always welcome 👏\n',
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sondrelg/flake8-typing-only-imports',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
