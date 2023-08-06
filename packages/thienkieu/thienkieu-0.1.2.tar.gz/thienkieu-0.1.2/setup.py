# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thienkieu']

package_data = \
{'': ['*']}

install_requires = \
['pyfiglet>=0.8.post1,<0.9']

setup_kwargs = {
    'name': 'thienkieu',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'DuyChu',
    'author_email': 'duycb92@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
