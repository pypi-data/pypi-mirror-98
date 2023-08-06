# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrudful']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scrudful',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'David Charboneau',
    'author_email': 'david@openteams.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/openteams/scrudful',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
