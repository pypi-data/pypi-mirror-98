# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['azureloggerbundle', 'azureloggerbundle.app_insights']

package_data = \
{'': ['*'], 'azureloggerbundle': ['_config/*']}

install_requires = \
['logger-bundle>=0.7.0b1',
 'opencensus-ext-azure>=1.0,<2.0',
 'opencensus>=0.7.7,<1.0.0',
 'pyfony-bundles>=0.4.0b1']

entry_points = \
{'pyfony.bundle': ['create = '
                   'azureloggerbundle.AzureLoggerBundle:AzureLoggerBundle']}

setup_kwargs = {
    'name': 'azure-logger-bundle',
    'version': '0.3.1b0',
    'description': 'Azure Logger bundle for the Pyfony framework',
    'long_description': 'Azure Logger bundle for the Pyfony Framework\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/azure-logger-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
