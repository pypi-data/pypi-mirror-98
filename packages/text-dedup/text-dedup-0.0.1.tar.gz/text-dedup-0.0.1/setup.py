# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_dedup', 'text_dedup.dedupers']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=1.6.2,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pytest>=6.2.2,<7.0.0',
 'strsimpy>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'text-dedup',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Chenghao Mou',
    'author_email': 'mouchenghao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
