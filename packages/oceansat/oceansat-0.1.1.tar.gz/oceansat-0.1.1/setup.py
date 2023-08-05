# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oceansat']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0', 'scipy>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['satver = oceansat.commandline:version']}

setup_kwargs = {
    'name': 'oceansat',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Bror Jonsson',
    'author_email': 'brorfred@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
