# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['loggerbundle',
 'loggerbundle.extra',
 'loggerbundle.handler',
 'loggerbundle.stdout']

package_data = \
{'': ['*'], 'loggerbundle': ['_config/*']}

install_requires = \
['colorlog>=4.0,<5.0', 'pyfony-bundles>=0.4.0b1']

entry_points = \
{'pyfony.bundle': ['create = loggerbundle.LoggerBundle:LoggerBundle']}

setup_kwargs = {
    'name': 'logger-bundle',
    'version': '0.7.0b1',
    'description': 'Logger bundle for the Pyfony framework',
    'long_description': 'Logger bundle for the Pyfony Framework\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/logger-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
