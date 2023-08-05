# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyopenfisheries']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.5,<3.0']

setup_kwargs = {
    'name': 'pyopenfisheries',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Henry Kobin',
    'author_email': 'henry.kobin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
