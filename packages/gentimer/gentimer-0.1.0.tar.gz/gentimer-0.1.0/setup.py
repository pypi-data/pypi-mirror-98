# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gentimer']

package_data = \
{'': ['*']}

install_requires = \
['darglint>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'gentimer',
    'version': '0.1.0',
    'description': 'Utility to make generator to be consumed in event-loop timer',
    'long_description': None,
    'author': 'teamikl',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
