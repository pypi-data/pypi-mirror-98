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
    'version': '1.0.1',
    'description': 'A language localization generator for Minecraft',
    'long_description': '![](https://img.shields.io/github/license/orangeutan/babelbox)\n![](https://img.shields.io/badge/python-3.8|3.9-blue)\n[![](https://img.shields.io/pypi/v/babelbox)](https://pypi.org/project/babelbox/)\n![](./coverage.svg)\n![](https://img.shields.io/badge/mypy-checked-green)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![](https://img.shields.io/badge/pre--commit-enabled-green)\n![](https://github.com/orangeutan/babelbox/workflows/test/badge.svg)\n\n# Babelbox\nBabelbox allows you to write your language files in the CSV format and then generate Minecraft language files from them.<br>\nCreating translations in CSV gives you an easy overview over any errors or missing languages.<br>\n\n## Install\n`pip install bablebox`\n\n## Usage\n`babelbox <src_dir> [dest_dir]`<br>\nFinds all `.csv` files in the source directory and generates minecraft language files\n\n# Example\nLets assume we have two csv files "items.csv" and "blocks.csv" in the folder "resourcepack/assets/minecraft/lang":\n\n| String             | en       | de         |\n| ------------------ | -------- | ---------- |\n| item.stick.name    | stick    | Stock      |\n| item.snowball.name | snowball | Schneeball |\n\n| String             | en      | de      |\n| ------------------ | ------- | ------- |\n| block.grass.name   | grass   | Gras    |\n| block.diamond.name | diamond | Diamant |\n\nLets run `babelbox resourcepack/assets/minecraft/lang`<br>\nBabelbox will now create the two language files "en.json" and "de.json" in the folder "resourcepack/assets/minecraft/lang":<br>\n```json\n{\n    "item.stick.name": "stick",\n    "item.snowball.name": "snowball",\n    "block.grass.name": "grass",\n    "block.diamond.name": "diamond"\n}\n```\n```json\n{\n    "item.stick.name": "Stock",\n    "item.snowball.name": "Schneeball",\n    "block.grass.name": "Gras",\n    "block.diamond.name": "Diamant"\n}\n```\n',
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
