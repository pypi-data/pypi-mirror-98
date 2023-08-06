# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiostore']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'aiostore',
    'version': '0.1.0',
    'description': 'Async abstraction layer for interchangeable file and object storage backends.',
    'long_description': None,
    'author': 'Oscar Linderoth',
    'author_email': 'oscar@upsidedev.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
