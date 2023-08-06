# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gentimer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gentimer',
    'version': '0.1.1',
    'description': 'Utility to make generator to be consumed in event-loop timer',
    'long_description': None,
    'author': 'teamikl',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/teamikl/gentimer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
