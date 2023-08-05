# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ruthie', 'ruthie.commands', 'ruthie.toolset']

package_data = \
{'': ['*']}

install_requires = \
['docopt==0.6.2', 'toml>=0.9', 'xmlrunner>=1.7.7,<1.8.0']

entry_points = \
{'console_scripts': ['ruthie = ruthie.cli:main']}

setup_kwargs = {
    'name': 'ruthie',
    'version': '0.1.3',
    'description': 'Run Unit Tests Harmoniously Incredibly Easy',
    'long_description': '# Ruthie\n\n[![Current Release](https://img.shields.io/github/release/bitbar/ruthie.svg)](releases)\n[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](LICENSE.md)\n\n<div align="center">\n\t<img height="256" src=".static/logo.png" alt="Ruthie Logo">\n</div>\n\nRuthie is the Unittests runner, and it\'s an acronym from "Run Unit Tests Harmoniously Incredibly Easy". \n\n## Installation\n\n```sh\npip install -U ruthie\n```\n\nCheck if it works:\n\n```sh\nruthie --version\n> 0.1.2\n```\n\n## Usage\n\nType `ruthie --help` to display available commands and options\n\n### Examples\n\n#### List all test classes in directory "unittests"\n\n```sh\nruthie discover classes unittests\n```\n\nOutput:\n\n```sh\nunittests.admin_panel.users.Add\nunittests.admin_panel.users.Edit\nunittests.admin_panel.users.Delete\nunittests.admin_panel.devices.Add\nunittests.admin_panel.devices.Edit\nunittests.admin_panel.devices.Delete\nunittests.end_user.projects.Add\nunittests.end_user.projects.Edit\nunittests.end_user.projects.Delete\n```\n\n#### List all test classes in directory "unittests" and group them\n\n```sh\nruthie discover classes unittests --group\n```\n\nOutput:\n\n```sh\n  unittests.admin_panel.users\n    Add\n    Edit\n    Delete\n  unittests.admin_panel.devices\n    Add\n    Edit\n    Delete\n  unittests.end_user.projects\n    Add\n    Edit\n    Delete\n```\n\n#### Discover all classes in directory "unittests" and run them in parallel using 10 threads\n\n```sh\nruthie parallel --threads=10 unittests\n```\n\n## License\n\nThis project is licensed under the ISC License - see the [LICENSE](LICENSE) file for details.\n',
    'author': 'Marek Sierociński',
    'author_email': 'marek.sierocinski@smartbear.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bitbar/ruthie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
