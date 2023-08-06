# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['babelbox']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['babelbox = babelbox.__main__:app']}

setup_kwargs = {
    'name': 'babelbox',
    'version': '1.0.0',
    'description': 'A language localization generator for Minecraft',
    'long_description': '# Babelbox\nA language localization generator for Minecraft\n',
    'author': 'Oran9eUtan',
    'author_email': 'Oran9eUtan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OrangeUtan/babelbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
