# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maquette', 'maquette.common', 'maquette_lib']

package_data = \
{'': ['*']}

install_requires = \
['chevron>=0.14.0,<0.15.0',
 'click>=7.1.2,<8.0.0',
 'gitpython>=3.1.12,<4.0.0',
 'pandas>=1.0.0,<2.0.0',
 'pandavro>=1.5.2,<2.0.0',
 'pylint>=2.7.2,<3.0.0',
 'pytest>=6.2.2,<7.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'seaborn>=0.11.0,<0.12.0']

entry_points = \
{'console_scripts': ['mq = maquette.cli:mq', 'unix_env = unix_env:unix_env']}

setup_kwargs = {
    'name': 'maquette',
    'version': '0.1.6',
    'description': 'A command line interface for Maquette Data Science and Machine Learning Platform.',
    'long_description': '# Maquette Py\n\nThis project contains the Python implementation of Maquette which includes the CLI and a SDK\n\n\n## Developing maquette-py\n\n`maquette-py` uses [Poetry](https://python-poetry.org/) for dependency management and is packaged with [PyInstaller](https://www.pyinstaller.org/). The minimal requirements for a developer workspace are [Conda](https://docs.conda.io/en/latest/miniconda.html) and [Poetry](https://python-poetry.org/docs/#installation).\n\n```\n$ git clone $REPOSITORY_URL\n$ cd maquette-py\n$ conda create -p ./environment python=3.8\n\n$ poetry install\n```\n\n## Maquette CLI\nThe CLI is documented within the CLI. Sounds funny but a good starting point is following command\n```\n$ mq --help\n```\n###Projects\n#### Report Code Quality\n```\n$ mq projects report-cq [packge_names, script.py, ...]\n```\nthe `report-cq` command sends code quality information to the Maquette Hub...\n\nto report the Pytest-Coverage, pytest has to be run previously with following parameters\n```\n$ python -m pytest cov=<your-packages> > test/test-report.log\n```\n\n## Maquette SDK',
    'author': 'Johannes Forster',
    'author_email': 'johannesforster@kpmg.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
