# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kt_tr']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['tr = kt_tr.cli:cli']}

setup_kwargs = {
    'name': 'kt-tr',
    'version': '0.2.0',
    'description': 'Calcula as regioes de um trading range',
    'long_description': '# kt-tr',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vfranca/kt-tr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
