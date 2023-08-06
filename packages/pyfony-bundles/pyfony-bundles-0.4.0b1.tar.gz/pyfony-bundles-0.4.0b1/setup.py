# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyfonybundles', 'pyfonybundles.loader']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=3.3,<4.0',
 'injecta>=0.10.0b1',
 'python-box>=3.4,<4.0',
 'tomlkit>=0.5.8,<1.0.0']

setup_kwargs = {
    'name': 'pyfony-bundles',
    'version': '0.4.0b1',
    'description': 'Pyfony Framework bundles base package',
    'long_description': 'Pyfony Framework bundles base package',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/pyfony-bundles',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
