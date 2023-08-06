# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uquake', 'uquake.grid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'uquake.grid',
    'version': '0.1.0',
    'description': 'grid utility for uQuake',
    'long_description': None,
    'author': 'jpmercier',
    'author_email': 'jpmercier01@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
