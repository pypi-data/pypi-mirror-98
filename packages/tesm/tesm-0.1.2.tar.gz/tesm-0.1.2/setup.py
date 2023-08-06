# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tesm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tesm',
    'version': '0.1.2',
    'description': 'Pseudo-assembly programming-like language',
    'long_description': None,
    'author': 'Ruthenic',
    'author_email': 'mdrakea3@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
