# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcanitexgen']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'numpy>=1.20.1,<2.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'mcanitexgen',
    'version': '0.1.0',
    'description': 'A texture animation generator for Minecraft .mcmeta files',
    'long_description': None,
    'author': 'Oran9eUtan',
    'author_email': 'oran9eutan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
