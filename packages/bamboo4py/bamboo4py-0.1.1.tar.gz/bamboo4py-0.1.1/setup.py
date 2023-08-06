# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bamboo4py', 'bamboo4py.drivers']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.11,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'netaddr>=0.8.0,<0.9.0',
 'pyyaml>=5.4.1,<6.0.0',
 'validobj>=0.3.11,<0.4.0']

entry_points = \
{'console_scripts': ['bamboo4py = bamboo4py.main']}

setup_kwargs = {
    'name': 'bamboo4py',
    'version': '0.1.1',
    'description': 'PyBamboo (python-bamboo) is original bamboo implementation in python',
    'long_description': None,
    'author': 'thisLight',
    'author_email': 'l1589002388@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
