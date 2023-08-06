# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tesm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tesm',
    'version': '0.1.4',
    'description': 'Pseudo-assembly programming-like language',
    'long_description': "hello welcome to tesm  \n# Instructions\ndownload python  \nwrite the tesm code  \nensure python is installed  \nrun the interpreter in the console with `python main.py tesm_file.tesm`  \nmake sure python is installed    \nyou have now learnt how to use the most epicness language ~~and/or sin~~ in the world, congrats  \nnow you just have to make sure that you have python installed  \n# Notes\ncompatibilty with anything that isn't Linux is not guaranteed \n",
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
