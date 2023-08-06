# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdcode']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0', 'parsy>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['zake = zdcode.program:main_zake',
                     'zdcode = zdcode.program:main']}

setup_kwargs = {
    'name': 'zdcode',
    'version': '2.12.1',
    'description': 'A ZDoom DECORATE transpiler and mod content build system',
    'long_description': None,
    'author': 'Gustavo6046',
    'author_email': 'rehermann6046@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
