# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blacksquare']

package_data = \
{'': ['*']}

install_requires = \
['frozendict>=1.2,<2.0',
 'numpy>=1.19.4,<2.0.0',
 'pdfkit>=0.6.1,<0.7.0',
 'puzpy>=0.2.5,<0.3.0',
 'pypdf2>=1.26.0,<2.0.0',
 'tqdm>=4.55.1,<5.0.0']

setup_kwargs = {
    'name': 'blacksquare',
    'version': '0.1.0',
    'description': 'A package for creating crossword puzzles',
    'long_description': None,
    'author': 'Patrick Maher',
    'author_email': 'pmaher86@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
