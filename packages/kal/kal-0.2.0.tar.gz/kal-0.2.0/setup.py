# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kal', 'kal.base', 'kal.commands', 'kal.utils']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0', 'cookiecutter>=1.7.2,<2.0.0', 'pend>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['kal = kal.runner:main']}

setup_kwargs = {
    'name': 'kal',
    'version': '0.2.0',
    'description': 'Personal assistant cli tool',
    'long_description': None,
    'author': 'joyongjin',
    'author_email': 'wnrhd114@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
