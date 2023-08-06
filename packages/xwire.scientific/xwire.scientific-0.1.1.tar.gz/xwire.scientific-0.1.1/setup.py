# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xwire',
 'xwire.scientific',
 'xwire.scientific._private',
 'xwire.scientific._private.math',
 'xwire.scientific.public']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xwire.scientific',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'tylerlaberge',
    'author_email': 'tylerlaberge@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
