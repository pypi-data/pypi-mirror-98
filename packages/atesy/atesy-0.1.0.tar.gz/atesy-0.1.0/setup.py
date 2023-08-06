# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atesy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'atesy',
    'version': '0.1.0',
    'description': 'Placeholder package',
    'long_description': None,
    'author': 'Piotr Falkowski',
    'author_email': 'piotr.falkowski@zf.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
