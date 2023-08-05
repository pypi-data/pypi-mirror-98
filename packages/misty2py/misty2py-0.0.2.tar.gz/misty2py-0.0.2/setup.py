# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['misty2py']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'websocket-client>=0.58.0,<0.59.0']

setup_kwargs = {
    'name': 'misty2py',
    'version': '0.0.2',
    'description': 'Misty II REST API wrapper',
    'long_description': None,
    'author': "Chris 'Scar(R)ed' Vajdik",
    'author_email': 'scarred.chris@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
