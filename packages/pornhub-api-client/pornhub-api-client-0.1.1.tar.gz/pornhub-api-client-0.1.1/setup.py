# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pornhub', 'pornhub.tests']

package_data = \
{'': ['*'], 'pornhub.tests': ['responses/*', 'schemas/*']}

entry_points = \
{'console_scripts': ['phb = pornhub.client:main',
                     'run-tests = pornhub.tests.unit_test:main']}

setup_kwargs = {
    'name': 'pornhub-api-client',
    'version': '0.1.1',
    'description': 'Simple lib to work with pornhub API',
    'long_description': None,
    'author': 'Misha Bystrov',
    'author_email': 'drudkhmisha@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
