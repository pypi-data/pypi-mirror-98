# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['info_gtk', 'info_gtk.data_individu']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=7.1.2,<8.0.0',
 'openpyxl>=3.0.5,<4.0.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'info-gtk',
    'version': '0.1.0',
    'description': 'CLI / SDK python info-gtk',
    'long_description': None,
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
