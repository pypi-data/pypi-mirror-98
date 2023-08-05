# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['projmap']

package_data = \
{'': ['*'], 'projmap': ['data/*']}

install_requires = \
['cartopy>=0.18.0',
 'cython>=0.29.21,<0.30.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.15,<2.0',
 'pyshp>=2.1.0,<3.0.0',
 'scipy>=1.3,<2.0',
 'six>=1.12,<2.0']

setup_kwargs = {
    'name': 'projmap',
    'version': '0.89',
    'description': 'High level wrapper of matplotlibs mapping package',
    'long_description': None,
    'author': 'Bror Jonsson',
    'author_email': 'brorfred@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
