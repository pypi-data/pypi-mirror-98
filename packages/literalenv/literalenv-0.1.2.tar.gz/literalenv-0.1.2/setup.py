# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['literalenv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'literalenv',
    'version': '0.1.2',
    'description': 'Parses an environment variable as a Python literal and outputs it to stdout.',
    'long_description': None,
    'author': 'Ellis Percival',
    'author_email': 'literalenv@failcode.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
