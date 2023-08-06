# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mancala', 'mancala.envs']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.18.0,<0.19.0', 'numpy>=1.20.1,<2.0.0']

entry_points = \
{'console_scripts': ['mancala = mancala.cli:cli']}

setup_kwargs = {
    'name': 'mancala',
    'version': '0.1.0',
    'description': 'Mancala written in Python, playable in CLI (GUI coming soon)!',
    'long_description': None,
    'author': 'Qiushi Pan',
    'author_email': 'qiu.gits@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
