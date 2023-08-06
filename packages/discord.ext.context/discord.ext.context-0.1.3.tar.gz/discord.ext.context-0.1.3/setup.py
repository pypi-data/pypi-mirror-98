# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ext', 'ext.context']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'discord.ext.context',
    'version': '0.1.3',
    'description': 'Globally accessable context for discord.py events.',
    'long_description': None,
    'author': 'scragly',
    'author_email': '29337040+scragly@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
