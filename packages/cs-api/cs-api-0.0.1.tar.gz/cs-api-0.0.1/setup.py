# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cs_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cs-api',
    'version': '0.0.1',
    'description': 'reservation',
    'long_description': None,
    'author': 'Jonas Krüger Svensson',
    'author_email': 'jonas-ks@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
