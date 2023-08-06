# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['whoiam']
setup_kwargs = {
    'name': 'whoiam',
    'version': '1.0.0',
    'description': 'WhoIAm()',
    'long_description': None,
    'author': 'None',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
