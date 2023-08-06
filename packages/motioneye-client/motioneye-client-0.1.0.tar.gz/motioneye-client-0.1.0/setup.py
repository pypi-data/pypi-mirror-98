# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['motioneye_client']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'motioneye-client',
    'version': '0.1.0',
    'description': 'motionEye client library Python Package',
    'long_description': None,
    'author': 'Dermot Duffy',
    'author_email': 'dermot.duffy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dermotduffy/motioneye-client',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
