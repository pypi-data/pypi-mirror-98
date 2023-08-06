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
    'version': '1.2.0',
    'description': 'A language localization generator for Minecraft',
    'long_description': '![](https://img.shields.io/github/license/orangeutan/babelbox)\n![](https://img.shields.io/badge/python-3.8|3.9-blue)\n[![](https://img.shields.io/pypi/v/babelbox)](https://pypi.org/project/babelbox/)\n![](https://raw.githubusercontent.com/OrangeUtan/babelbox/cabe03f93500e0ee2e0bf9f39c03e52007989ecb/coverage.svg)\n![](https://img.shields.io/badge/mypy-checked-green)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![](https://img.shields.io/badge/pre--commit-enabled-green)\n![](https://github.com/orangeutan/babelbox/workflows/test/badge.svg)\n\n# Babelbox\nBabelbox allows you to write your language files in the CSV format and then generate Minecraft language files from them.<br>\nCreating translations in CSV gives you an easy overview over any errors or missing languages.<br>\n\n# Table of contents\n- [Installation](#Installation)\n- [Usage](#Usage)\n- [Examples](#Examples)\n    - [Basic usage](#Basic-usage)\n    - [Shorten variable names](#Shorten-variable-names)\n- [Changelog](https://github.com/OrangeUtan/babelbox/blob/main/CHANGELOG.md)\n\n# Installation\n```\npip install babelbox\n```\n\n# Usage\nFinds all `.csv` files in the source directory and generates minecraft language files<br>\n```\nbabelbox <src_dir> [dest_dir]\n    -p, --pretty-print      Pretty print json\n    -i, -indent TEXT        String used to indent json\n    -n, --prefix-filename   Prefixes all variables with filename\n    --dry                   Dry run. Don\'t create any files\n    -v, --verbose\n```\n\n# Examples\n## Basic usage:\nWe have these two CSV files containing our translations:\n\n**.../lang/items.csv:**\n| Variable           | en_us    | de_de      |\n| ------------------ | -------- | ---------- |\n| item.stick.name    | stick    | Stock      |\n| item.snowball.name | snowball | Schneeball |\n\n**.../lang/blocks.csv:**\n| Variable           | en_us   | de_de   |\n| ------------------ | ------- | ------- |\n| block.grass.name   | grass   | Gras    |\n| block.diamond.name | diamond | Diamant |\n\nRunning `babelbox .../lang/` makes Babelbox parse the CSV files and generate the following language files in the same folder:<br>\n**.../lang/en_us.json:**\n```json\n{\n    "item.stick.name": "stick",\n    "item.snowball.name": "snowball",\n    "block.grass.name": "grass",\n    "block.diamond.name": "diamond"\n}\n```\n**.../lang/de_de.json:**\n```json\n{\n    "item.stick.name": "Stock",\n    "item.snowball.name": "Schneeball",\n    "block.grass.name": "Gras",\n    "block.diamond.name": "Diamant"\n}\n```\n\n## Shorten variable names:\nWe can use the `--prefix-filename` flag to save ourselve some typing. If all variables in a CSV file share a common prefix, we can name the file to that prefix and let Babelbox prepend it.\n\n**.../lang/item.swords.csv**\n| Variable     | en_us         | de_de          |\n| ------------ | ------------- | -------------- |\n| diamond.name | Diamond Sword | Diamantschwert |\n| gold.name    | Gold sword    | Goldschwert    |\n\nRunning `babelbox .../lang/ --prefix-filename` creates these two files:\n\n**.../lang/en_us.json**\n```json\n{\n    "item.swords.diamond.name": "Diamond Sword",\n    "item.swords.gold.name": "Gold sword",\n}\n```\n**.../lang/de_de.json**\n```json\n{\n    "item.swords.diamond.name": "Diamantschwert",\n    "item.swords.gold.name": "Goldschwert",\n}\n```\n\nAll variables have been prefixed with **item.swords**\n',
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
