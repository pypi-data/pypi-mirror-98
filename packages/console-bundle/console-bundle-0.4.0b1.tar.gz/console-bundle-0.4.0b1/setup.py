# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['consolebundle']

package_data = \
{'': ['*'], 'consolebundle': ['_config/*']}

install_requires = \
['colorlog>=4.0,<5.0',
 'pyfony-bundles>=0.4.0b1',
 'pyfony-core>=0.8.0b1',
 'python-dotenv>=0.13.0,<1.0.0']

entry_points = \
{'console_scripts': ['console = consolebundle.CommandRunner:run_command'],
 'pyfony.bundle': ['create = consolebundle.ConsoleBundle:ConsoleBundle']}

setup_kwargs = {
    'name': 'console-bundle',
    'version': '0.4.0b1',
    'description': 'Console Bundle for the Pyfony Framework',
    'long_description': 'Console Bundle for the Pyfony Framework\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/console-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
