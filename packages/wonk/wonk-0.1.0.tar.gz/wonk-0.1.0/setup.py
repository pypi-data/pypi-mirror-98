# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wonk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wonk',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Kirk Strauser',
    'author_email': 'kirk@amino.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
