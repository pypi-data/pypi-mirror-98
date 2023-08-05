# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpyefficient']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0', 'numpy>=1.19', 'openpyxl>=3.0', 'pandas>=1']

setup_kwargs = {
    'name': 'jrpyefficient',
    'version': '0.0.0',
    'description': 'Jumping Rivers: Efficient Data Science in Python',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
