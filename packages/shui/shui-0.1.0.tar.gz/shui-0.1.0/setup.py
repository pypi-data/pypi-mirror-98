# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shui', 'shui.api', 'shui.commands']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'cleo>=0.8.1,<0.9.0',
 'packaging>=20.9,<21.0',
 'requests>=2.25.1,<3.0.0',
 'url-normalize>=1.4.3,<2.0.0']

entry_points = \
{'console_scripts': ['shui = shui.cli:main']}

setup_kwargs = {
    'name': 'shui',
    'version': '0.1.0',
    'description': 'Spark-Hadoop Installer For Linux',
    'long_description': None,
    'author': 'James Robinson',
    'author_email': 'james.em.robinson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
