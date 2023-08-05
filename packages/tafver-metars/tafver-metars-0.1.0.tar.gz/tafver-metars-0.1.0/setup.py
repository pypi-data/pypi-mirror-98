# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tafver_metars']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=7.1.2,<8.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.13.0,<10.0.0']

entry_points = \
{'console_scripts': ['tafver = tafver_metars.__main__:main']}

setup_kwargs = {
    'name': 'tafver-metars',
    'version': '0.1.0',
    'description': "Download and formating METAR's and TAF's as a input for TAF-VER software verificator.",
    'long_description': None,
    'author': 'diego-garro',
    'author_email': 'diego.garromolina@yahoo.com',
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
