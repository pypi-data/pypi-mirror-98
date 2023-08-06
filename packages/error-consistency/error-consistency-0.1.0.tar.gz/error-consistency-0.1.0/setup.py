# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['error_consistency']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.4,<4.0.0',
 'numba>=0.52.0,<0.53.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'ray[tune]>=1.2.0,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'seaborn>=0.11.1,<0.12.0',
 'sphinx-rtd-theme>=0.5.1,<0.6.0',
 'tqdm>=4.56.0,<5.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'error-consistency',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Derek M Berger',
    'author_email': 'dmberger.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
