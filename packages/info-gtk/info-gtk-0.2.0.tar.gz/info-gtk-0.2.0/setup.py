# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['info_gtk', 'info_gtk.data_individu']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'bs4>=0.0.1,<0.0.2',
 'click>=7.1.2,<8.0.0',
 'json5>=0.9.5,<0.10.0',
 'openpyxl>=3.0.5,<4.0.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'info-gtk',
    'version': '0.2.0',
    'description': 'CLI / SDK python info-gtk',
    'long_description': '# Info GTK CLI\n\n[![PyPi Package Version](https://img.shields.io/pypi/v/info-gtk)](https://pypi.org/project/info-gtk/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/info-gtk)](https://pypi.org/project/info-gtk/)\n[![LICENSE](https://img.shields.io/github/license/dapodix/info-gtk)](https://github.com/dapodix/info-gtk/blob/main/LICENSE)\n[![Tests](https://github.com/dapodix/info-gtk/workflows/Tests/badge.svg)](https://github.com/dapodix/info-gtk/actions?query=workflow%3ATests)\n[![codecov](https://codecov.io/gh/dapodix/info-gtk/branch/main/graph/badge.svg)](https://codecov.io/gh/dapodix/info-gtk)\n\nCLI / SDK python [info-gtk](https://info.gtk.kemdikbud.go.id/).\n\n## Fitur yang akan datang\n\nBerikut fitur yang akan direncanakan untuk aplikasi ini.\n\n- Export data ke excel\n- Download / Print masal\n\n## Donasi\n\nJika anda ingin melakukan donasi untuk kami, bisa menghubungi kami melalui [WhatsApp](https://wa.me/6287725780404) ataupun [Telegram](https://t.me/hexatester).\n\n## Legal / Hukum\n\nKode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh Kemdikbud atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. _Gunakan dengan risiko Anda sendiri_.\n',
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
