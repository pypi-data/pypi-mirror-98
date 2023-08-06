# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tafver_metars']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=7.1.2,<8.0.0',
 'metar>=1.8.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.13.0,<10.0.0']

entry_points = \
{'console_scripts': ['tafver = tafver_metars.__main__:taf_ver']}

setup_kwargs = {
    'name': 'tafver-metars',
    'version': '0.3.1',
    'description': "Download and formating METAR's and TAF's as an input for TAF-VER software verificator.",
    'long_description': "# TAFVER METARS\n\nSimple command line tool to download METAR's and TAF's for a given station.\n\n## Installation\n\nFor install only run this command from your terminal\n\n```\npip install tafver-metars\n```\n\n### Update\n\nUpdate with `pip` adding the option --upgrade\n\n```\npip install --upgrade tafver-metars\n```\n\n## Examples\n\nTo download data from the current month for JFK INT. Airport only run \n\n```\ntafver download kjfk\n```\n\nIf you need older month but the same year run\n\n```\ntafver download kjfk -m 2\n```\n\nwhere `-m 2` its an option and refers to february. Take in count that this value must be\nearlier than the actual month for the same year.\n\nIf you need older year run\n\n```\ntafver download kjfk -y 2020\n```\n\nwhere `-y 2020` its an option and refers to the year 2020. Take in count that the year must be\nolder than 2004, only years from 2005 onwards are allowed. That's because only this years are\navailable in databases of Ogimet.com. ",
    'author': 'diego-garro',
    'author_email': 'diego.garromolina@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diego-garro/tafver-metars',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
