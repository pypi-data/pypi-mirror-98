# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devhelpers']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx-autodoc-typehints>=1.11.1,<2.0.0',
          'Sphinx>=3.5.1,<4.0.0',
          'numpydoc>=1.1.0,<2.0.0']}

setup_kwargs = {
    'name': 'devhelpers',
    'version': '0.1.1',
    'description': 'A Development Toolbox',
    'long_description': '![GitHub](https://img.shields.io/github/license/MichaelSasser/devhelpers?style=flat-square)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/MichaelSasser/devhelpers/Build%20and%20Tests?style=flat-square)\n\n# DevHelpers\n\nDevHelpers is a loose collection of python development helpers.\nIt is not made to be included or used in a finished product.\n\n# Toolbox\n\n- The `@timeit` decorator to time the runtime of a function or method.\n  With `@timit(1000)` the function or method will be timed 1000 times\n  and prints afterword a small statistic.\n\n## Semantic Versioning\n\nThis repository uses [SemVer](https://semver.org/) for its release cycle.\n\n## Branching Model\n\nThis repository uses the\n[git-flow](https://danielkummer.github.io/git-flow-cheatsheet/index.html)\nbranching model by [Vincent Driessen](https://nvie.com/about/). It has two branches with infinite lifetime:\n\n* [master](https://github.com/MichaelSasser/devhelpers/tree/master)\n* [develop](https://github.com/MichaelSasser/devhelpers/tree/develop)\n\nThe master branch gets updated on every release. The develop branch is the merging branch.\n\n## License\n\nCopyright &copy; 2021 Michael Sasser <Info@MichaelSasser.org>. Released under the GPLv3 license.\n',
    'author': 'Michael Sasser',
    'author_email': 'Michael@MichaelSasser.org',
    'maintainer': 'Michael Sasser',
    'maintainer_email': 'Michael@MichaelSasser.org',
    'url': 'https://github.com/MichaelSasser/devhelpers',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
