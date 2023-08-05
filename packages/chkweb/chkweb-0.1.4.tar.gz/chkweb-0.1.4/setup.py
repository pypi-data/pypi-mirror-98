# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['chkweb']
install_requires = \
['fire>=0.4.0,<0.5.0', 'prettyconf>=2.2.1,<3.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'chkweb',
    'version': '0.1.4',
    'description': 'A very simple web crawler and checker',
    'long_description': None,
    'author': 'Juan Ignacio Rodriguez de Leon',
    'author_email': 'euribates@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
