# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['base45']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['base45 = base45.cli:main']}

setup_kwargs = {
    'name': 'base45',
    'version': '0.1.0',
    'description': 'Base45 Encoder/Decoder',
    'long_description': None,
    'author': 'Jakob Schlyter',
    'author_email': 'jakob@kirei.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
