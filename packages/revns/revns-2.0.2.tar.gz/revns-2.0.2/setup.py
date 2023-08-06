# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['revns']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'revns',
    'version': '2.0.2',
    'description': '',
    'long_description': None,
    'author': 'Chien',
    'author_email': 'a0186163@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
