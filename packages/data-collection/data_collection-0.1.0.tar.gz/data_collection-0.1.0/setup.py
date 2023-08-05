# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_collection',
 'data_collection.face_recognition',
 'data_collection.scripts']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'dlib>=19.21.1,<20.0.0',
 'face_recognition_models>=0.3.0,<0.4.0',
 'fire>=0.4.0,<0.5.0',
 'numpy>=1.20.1,<2.0.0',
 'tqdm>=4.59.0,<5.0.0']

entry_points = \
{'console_scripts': ['data_collection = data_collection.cli:fire_main']}

setup_kwargs = {
    'name': 'data-collection',
    'version': '0.1.0',
    'description': 'Collection of scripts for compiling various forms of data for ML',
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
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
