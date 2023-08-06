# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modoo']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0', 'openpyxl>=3.0.7,<4.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['mdcli = modoo.cli:main']}

setup_kwargs = {
    'name': 'modoo',
    'version': '0.1.2',
    'description': 'a CLI tool set for Modoo Corpus build',
    'long_description': None,
    'author': 'Yeonwoo Kim',
    'author_email': 'wiskingdom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
