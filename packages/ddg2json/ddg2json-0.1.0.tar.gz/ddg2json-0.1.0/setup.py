# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ddg2json']

package_data = \
{'': ['*']}

install_requires = \
['BeautifulSoup>=4.9.3,<5.0.0']

entry_points = \
{'console_scripts': ['ddg2json = ddg2json:main']}

setup_kwargs = {
    'name': 'ddg2json',
    'version': '0.1.0',
    'description': 'Parses the HTML of DuckDuckGo pages into JSON',
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
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
