# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['play_takeout_to_plex']

package_data = \
{'': ['*']}

install_requires = \
['eyed3>=0.9.6,<0.10.0']

entry_points = \
{'console_scripts': ['play2plex = play_takeout_to_plex:main']}

setup_kwargs = {
    'name': 'play-takeout-to-plex',
    'version': '0.1.1',
    'description': 'Re-name and re-structure google play music takeout to be plex friendly',
    'long_description': None,
    'author': 'checkroth',
    'author_email': 'checkroth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Checkroth/play-takeout-to-plex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
