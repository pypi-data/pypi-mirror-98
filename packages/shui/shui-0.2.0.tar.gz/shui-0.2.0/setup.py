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
 'pathlib3x>=1.3.9,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.59.0,<5.0.0',
 'url-normalize>=1.4.3,<2.0.0']

entry_points = \
{'console_scripts': ['shui = shui.cli:main']}

setup_kwargs = {
    'name': 'shui',
    'version': '0.2.0',
    'description': 'Spark-Hadoop Unix Installer',
    'long_description': '# SHUI\nSpark-Hadoop Unix Installer\n\n![](https://img.shields.io/badge/system-macOS%7CLinux%7CFreeBSD-green)\n\n[![Python](https://img.shields.io/pypi/pyversions/shui.svg?logo=python&logoColor=white)](https://pypi.org/project/shui)\n\nThis package uses Python to download and unpack a pre-built version of Spark/Hadoop from Apache.\nIts primary use-case is simplifying unattended installs where the user wants "the latest available version" of these tools.\n\n## Features\n\n* download Spark/Hadoop release from Apache.\n* unpack the tarball to a target directory on your local system.\n\n## Installation\n\nFirst you\'ll need to install `shui` using pip: `pip install shui`. **Note** this requires `Python >= 3.6`.\n\n## Common usage examples\n\n### Versions\n\n```\nUSAGE\n  shui versions [--latest]\n\nOPTIONS\n  --latest               Show only the latest available version\n\nGLOBAL OPTIONS\n  -h (--help)            Display this help message\n  -q (--quiet)           Do not output any message\n  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug\n  -V (--version)         Display this application version\n  --ansi                 Force ANSI output\n  --no-ansi              Disable ANSI output\n  -n (--no-interaction)  Do not ask any interactive question\n```\n\n### Install\n\n```\nUSAGE\n  shui install [--latest] [--spark\xa0<...>] [--hadoop\xa0<...>] [--target\xa0<...>]\n\nOPTIONS\n  --latest               Use the latest available version\n  --spark                Spark version (default: "any")\n  --hadoop               Hadoop version (default: "any")\n  --target               Directory to install into (default: "cwd")\n\nGLOBAL OPTIONS\n  -h (--help)            Display this help message\n  -q (--quiet)           Do not output any message\n  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug\n  -V (--version)         Display this application version\n  --ansi                 Force ANSI output\n  --no-ansi              Disable ANSI output\n  -n (--no-interaction)  Do not ask any interactive question\n```\n',
    'author': 'James Robinson',
    'author_email': 'james.em.robinson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jemrobinson/shui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
