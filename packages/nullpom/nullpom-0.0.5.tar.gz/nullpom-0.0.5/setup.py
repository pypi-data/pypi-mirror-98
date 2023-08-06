# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nullpom']

package_data = \
{'': ['*']}

install_requires = \
['lightgbm>=3.1.1,<4.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'pandas>=1.2.3,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0']

setup_kwargs = {
    'name': 'nullpom',
    'version': '0.0.5',
    'description': 'test',
    'long_description': None,
    'author': 'tenajima',
    'author_email': 'tenajima@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
