# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crudgen', 'crudgen.abstracts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'crudgen',
    'version': '0.1.1',
    'description': 'a minimal CRUD code generator',
    'long_description': None,
    'author': 'pouria',
    'author_email': 'pooriazmn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
