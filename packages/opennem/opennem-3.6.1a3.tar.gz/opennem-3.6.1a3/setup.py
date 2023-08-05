# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opennem', 'opennem.settings', 'opennem.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'pandas>=1.2.2,<2.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.23.0,<3.0.0',
 'requests_cache>=0.5.2,<0.6.0']

entry_points = \
{'console_scripts': ['opennem = opennem.cli:main']}

setup_kwargs = {
    'name': 'opennem',
    'version': '3.6.1a3',
    'description': 'OpenNEM Australian Energy Data Python Client',
    'long_description': '# OpenNEM Energy Market Data Access\n\nThe OpenNEM project aims to make the wealth of public National Electricity Market (NEM) data more accessible to a wider audience.\n\nThis client library for Python enables accessing the Opennem API and data sets.\n\nProject homepage at https://opennem.org.au\n\nCurrently supports:\n\n- Australia NEM: https://www.nemweb.com.au/\n- Australia WEM (West Australia): http://data.wa.aemo.com.au/\n\n## Requirements\n\n- Python 3.8+ (see `.python-version` with `pyenv`)\n- Docker and `docker-compose` if you want to run the local dev stack\n\n## Quickstart\n\nWith poetry:\n\n```sh\n$ poetry install\n$ source .venv/bin/activate\n```\n\nWith pip + venv:\n\n```sh\n$ pip -m venv .venv\n$ pip install -r requirements.txt\n$ source .venv/bin/activate\n```\n\n## Install\n\nYou can install this project with python `pip`:\n\n```sh\n$ pip install opennempy\n```\n',
    'author': 'Dylan McConnell',
    'author_email': 'dylan.mcconnell@unimelb.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://opennem.org.au',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
