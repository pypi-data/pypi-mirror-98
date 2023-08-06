# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['motioneye_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'pytest-cov>=2.11.1,<3.0.0']

setup_kwargs = {
    'name': 'motioneye-client',
    'version': '0.1.1',
    'description': 'motionEye client library Python Package',
    'long_description': '[![Build Status](https://travis-ci.com/dermotduffy/motioneye-client.svg?branch=master)](https://travis-ci.com/dermotduffy/motioneye-client)\n[![Coverage](https://img.shields.io/codecov/c/github/dermotduffy/motioneye-client)](https://codecov.io/gh/dermotduffy/motioneye-client)\n\n# motionEye Client\n',
    'author': 'Dermot Duffy',
    'author_email': 'dermot.duffy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dermotduffy/motioneye-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
