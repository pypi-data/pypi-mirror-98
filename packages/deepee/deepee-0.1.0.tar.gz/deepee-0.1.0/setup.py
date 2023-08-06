# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepee']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'mypy>=0.812,<0.813',
 'torch>=1.8.0,<2.0.0',
 'torchvision>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'deepee',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Georgios Kaissis',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
