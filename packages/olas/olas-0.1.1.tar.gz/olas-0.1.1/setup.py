# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olas']

package_data = \
{'': ['*']}

install_requires = \
['Cartopy>=0.18.0,<0.19.0',
 'Cython>=0.29.22,<0.30.0',
 'dask>=2021.3.0,<2022.0.0',
 'geos>=0.2.3,<0.3.0',
 'matplotlib>=3.3.4,<4.0.0',
 'proj>=0.2.0,<0.3.0',
 'xarray>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'olas',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'jorge.perez',
    'author_email': 'j.perez@metocean.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
