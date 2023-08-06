# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyowo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyowo',
    'version': '1.0.0',
    'description': 'A Python library to translate text to OwO',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
