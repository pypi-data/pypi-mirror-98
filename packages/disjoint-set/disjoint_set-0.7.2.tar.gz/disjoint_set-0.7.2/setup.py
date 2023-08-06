# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['disjoint_set']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'disjoint-set',
    'version': '0.7.2',
    'description': 'Disjoint Set data structure implementation for Python',
    'long_description': '# disjoint-set\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/disjoint_set.svg)\n[![PyPI](https://img.shields.io/pypi/v/disjoint_set.svg)](https://pypi.org/project/disjoint-set/)\n![Coveralls](https://img.shields.io/coveralls/github/mrapacz/disjoint-set/master.svg)\n![PyPI - License](https://img.shields.io/pypi/l/disjoint_set.svg)\n\n[DisjointSet](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) (a.k.a. union–find data structure or merge–find set) implementation for Python.\n\n## Prerequisites\n\nThe only requirement is having Python 3 installed, you can verify this by running:\n```bash\n$ python --version\nPython 3.7.2\n```\n\n## Installation\n```\npip install disjoint-set\n```\n\nYou can verify you\'re running the latest package version by running:\n```python\n>>> import disjoint_set\n>>> disjoint_set.__version__\n\'0.7.2\'\n\n```\n\n## Usage\n\n```python\n>>> from disjoint_set import DisjointSet\n>>> ds = DisjointSet()\n>>> ds.find(1)\n1\n>>> ds.union(1,2)\n>>> ds.find(1)\n2\n>>> ds.find(2)\n2\n>>> ds.connected(1,2)\nTrue\n>>> ds.connected(1,3)\nFalse\n\n>>> "a" in ds\nFalse\n>>> ds.find("a")\n\'a\'\n>>> "a" in ds\nTrue\n\n>>> list(ds)\n[(1, 2), (2, 2), (3, 3), (\'a\', \'a\')]\n\n>>> list(ds.itersets())\n[{1, 2}, {3}, {\'a\'}]\n\n```\n\n## Contributing\n\nFeel free to open any issues on github.\n\n## Authors\n\n* [Maciej Rapacz](https://github.com/mrapacz/)\n\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n',
    'author': 'Maciej Rapacz',
    'author_email': 'mmrapacz@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrapacz/disjoint-set/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
