# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mydavorpkg']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'mydavorpkg',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jorge Lara',
    'author_email': 'larajorge11@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
