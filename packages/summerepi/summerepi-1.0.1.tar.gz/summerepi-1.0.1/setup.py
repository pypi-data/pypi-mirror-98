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
    'version': '1.0.1',
    'description': 'Summer is a compartmental disease modelling framework, written in Python. It provides a high-level API to build and run models.',
    'long_description': '# Summer: compartmental disease modelling in Python\n\n[![Automated Tests](https://github.com/monash-emu/summer/actions/workflows/tests.yml/badge.svg)](https://github.com/monash-emu/summer/actions/workflows/tests.yml)\n\nSummer is a compartmental disease modelling framework, written in Python. It provides a high-level API to build and run models. Features include:\n\n- A variety of inter-compartmental flows (infections, sojourn, fractional, births, deaths, imports)\n- Force of infection multipliers (frequency, density)\n- Post-processing of compartment sizes into derived outputs\n- Stratification of compartments, including:\n  - Adjustments to flow rates based on strata\n  - Adjustments to infectiousness based on strata\n  - Heterogeneous mixing between strata\n  - Multiple disease strains\n\n**[Documentation here](http://summerepi.com/)** with [code examples](http://summerepi.com/examples).\n\n[Available on PyPi](https://pypi.org/project/summerepi/) as `summerepi`.\n\n## Installation and Quickstart\n\nThis project is tested with Python 3.6.\nInstall the `summerepi` package from PyPI\n\n```bash\npip install summerepi\n```\n\nThen you can use the library to build and run models. See here for some examples:\n\n- [SIR model](http://summerepi.com/examples/sir-model.html)\n- [SEIR model](http://summerepi.com/examples/seir-model.html)\n\nYou will find a significant performance improvement in the ODE solver if you set `OMP_NUM_THREADS` before importing `summer` or `numpy`.\n\n```python\n# Set this in your Python script\nos.environ["OMP_NUM_THREADS"] = "1"\n\n# Do it before importing summer or numpy\nimport summer\n# ...\n```\n\n## Development\n\n[Poetry](https://python-poetry.org/) is used for packaging and dependency management.\nYou will need to install poetry to work on this codebase.\nSome common things to do as a developer working on this codebase:\n\n```bash\n# Install requirements\npoetry config virtualenvs.in-project true\npoetry shell\npoetry install\n\n# Get a virtualenv for running other stuff\npoetry shell\n\n# Publish to PyPI - use your PyPI credentials\npoetry publish --build\n\n# Add a new package\npoetry add\n\n# Run tests\npoetry shell\npytest -vv\n\n# Format Python code\nblack .\n```\n\n## Releases\n\n_TODO_\n\n## Documentation\n\nSphinx is used to automatically build reference documentation for this library.\nThe documentation is automatically built and deployed to [summerepi.com](http://summerepi.com/) whenever code is pushed to `master`.\n\nTo build and deploy\n\n```bash\n./docs/scripts/build.sh\n./docs/scripts/deploy.sh\n```\n\nTo work on docs locally\n\n```bash\n# ./docs/scripts/watch.sh # FIXME - endless recursion\n./docs/scripts/build.sh\n# In a separate terminal\n./docs/scripts/serve.sh\n# Visit http://localhost:8000/\n```\n',
    'author': 'James Trauer',
    'author_email': 'james.trauer@monash.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://summerepi.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
