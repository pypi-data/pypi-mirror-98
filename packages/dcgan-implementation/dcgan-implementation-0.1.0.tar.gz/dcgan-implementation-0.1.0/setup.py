# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dcgan_implementation']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0',
 'imageio>=2.9.0,<3.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'tensorflow>=2.4.1,<3.0.0']

entry_points = \
{'console_scripts': ['dcgan = dcgan.__main__:fire_']}

setup_kwargs = {
    'name': 'dcgan-implementation',
    'version': '0.1.0',
    'description': 'Simple DCGAN implementation for experimenting',
    'long_description': None,
    'author': 'Andy Jackson',
    'author_email': 'amjack100@gmail.com',
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
