# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codefellows', 'codefellows.cftester', 'codefellows.dsa']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'codefellows',
    'version': '0.4.0',
    'description': 'Commonly needed Python modules',
    'long_description': None,
    'author': 'codefellows',
    'author_email': 'jb@codefellows.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
