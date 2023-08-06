# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ddg2json']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.8']

entry_points = \
{'console_scripts': ['ddg2json = ddg2json:main']}

setup_kwargs = {
    'name': 'ddg2json',
    'version': '0.1.2',
    'description': 'Parses scraped HTML of DuckDuckGo pages into JSON',
    'long_description': None,
    'author': 'NightMachinary',
    'author_email': 'rudiwillalwaysloveyou@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
