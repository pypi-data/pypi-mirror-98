# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_typing_only_imports']

package_data = \
{'': ['*']}

entry_points = \
{'flake8.extension': ['TYO100 = flake8_typing_only_imports:Plugin']}

setup_kwargs = {
    'name': 'flake8-typing-only-imports',
    'version': '0.1.12',
    'description': 'A flake8 plugin that flags imports exclusively used for type annotations',
    'long_description': '<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://img.shields.io/pypi/v/flake8-typing-only-imports.svg" alt="Package version">\n</a>\n<a href="https://codecov.io/gh/sondrelg/flake8-typing-only-imports">\n    <img src="https://codecov.io/gh/sondrelg/flake8-typing-only-imports/branch/master/graph/badge.svg" alt="Code coverage">\n</a>\n<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://github.com/sondrelg/flake8-typing-only-imports/actions/workflows/testing.yml/badge.svg" alt="Test status">\n</a>\n<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Supported Python versions">\n</a>\n<a href="http://mypy-lang.org/">\n    <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">\n</a>\n\n# flake8-typing-only-imports\n\nA flake8 plugin to help you identify which imports to put into type-checking blocks.\n\nBeyond this, it will also help you manage forward references however you would like to.\n\n## Installation\n\n```shell\npip install flake8-typing-only-imports\n```\n\n## Active codes\n\n| Code   | Description                                         |\n|--------|-----------------------------------------------------|\n| TYO100 | Import should be moved to a type-checking block  |\n\n\n## Deactivated (by default) codes\n| Code   | Description                                         |\n|--------|-----------------------------------------------------|\n| TYO101 | Third-party import should be moved to a type-checking block |\n| TYO200 | Missing \'from \\_\\_future\\_\\_ import annotations\' import |\n| TYO201 | Annotation is wrapped in unnecessary quotes |\n| TYO300 | Annotation should be wrapped in quotes |\n| TYO301 | Annotation is wrapped in unnecessary quotes |\n\nIf you wish to activate any of these checks, you need to pass them to flake8\'s `select` argument ([docs](https://flake8.pycqa.org/en/latest/user/violations.html)).\n\n`TYO101` is deactivated by default, mostly because misplaced third party imports don\'t carry\nwith it the same level of consequence that local imports can have - they will\nnever lead to import circularity issues. Activating `TYO101` will mostly help the\ninitialization time of your app.\n\nPlease note, `TYO200s` and `TYO300s` are mutually exclusive. Don\'t activate both series.\nRead on for an in-depth explanation.\n\n## Motivation\n\nTwo common issues when annotating large code bases are:\n\n1. Import circularity issues\n2. Annotating not-yet-defined structures\n\nThese problems are largely solved by two Python features:\n\n1. Type checking blocks\n\n    <br>The builtin `typing` library, as of Python 3.7, provides a `TYPE_CHECKING` block you can put type annotation imports into (see [docs](https://docs.python.org/3/library/typing.html#constant)).\n\n    ```python\n    from typing import TYPE_CHECKING\n\n    if TYPE_CHECKING:\n        # this code is not evaluated at runtime\n        from foo import bar\n    ```\n\n\n\n2. Forward references\n    <br><br>\n\n    When you\'ve got unevaluated imports (in type checking block), or you try to reference not-yet-defined structures, forward references are the answer. They can be used, like this:\n    ```python\n    class Foo:\n        def bar(self) -> \'Foo\':\n            return Foo()\n    ```\n\n    And ever since [PEP563](https://www.python.org/dev/peps/pep-0563/#abstract) was implemented, you also have the option of doing this:\n    ```python\n    from __future__ import annotations\n\n    class Foo:\n        def bar(self) -> Foo:\n            return Foo()\n    ```\n\n   See [this](https://stackoverflow.com/questions/55320236/does-python-evaluate-type-hinting-of-a-forward-reference) excellent stackoverflow response explaining forward references, if you\'d like more context.\n\nWith that said, the aim of this plugin is to automate the management of type annotation\nimports (type-checking block import management), and keeping track of the forward references that become necessary as a consequence.\n\n\n## As a pre-commit hook\n\nYou can run this flake8 plugin as a [pre-commit](https://github.com/pre-commit/pre-commit) hook:\n\n```yaml\n- repo: https://gitlab.com/pycqa/flake8\n  rev: 3.7.8\n  hooks:\n  - id: flake8\n    additional_dependencies: [flake8-typing-only-imports]\n```\n\n## Supporting the project\n\nLeave a&nbsp;⭐️&nbsp; if this project helped you!\n\nContributions are always welcome 👏\n',
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sondrelg/flake8-typing-only-imports',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
