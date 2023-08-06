# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['summer',
 'summer.legacy',
 'summer.legacy.flow',
 'summer.legacy.flow.base',
 'summer.legacy.model',
 'summer.legacy.model.utils']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0',
 'networkx==2.5',
 'numba>=0.52.0,<0.53.0',
 'numpy==1.19.5',
 'scipy==1.1.0']

setup_kwargs = {
    'name': 'summerepi',
    'version': '1.0.0',
    'description': 'Summer is a compartmental disease modelling framework, written in Python. It provides a high-level API to build and run models.',
    'long_description': None,
    'author': 'James Trauer',
    'author_email': 'james.trauer@monash.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
