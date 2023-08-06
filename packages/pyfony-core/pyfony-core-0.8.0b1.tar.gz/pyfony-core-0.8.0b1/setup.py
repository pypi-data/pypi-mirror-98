# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyfonycore',
 'pyfonycore.bootstrap',
 'pyfonycore.bootstrap.config',
 'pyfonycore.bootstrap.config.raw',
 'pyfonycore.container']

package_data = \
{'': ['*'], 'pyfonycore': ['_config/*']}

install_requires = \
['injecta>=0.10.0b1', 'pyfony-bundles>=0.4.0b1']

setup_kwargs = {
    'name': 'pyfony-core',
    'version': '0.8.0b1',
    'description': 'Pyfony core',
    'long_description': '# Pyfony Core\n\nPart of the [Pyfony Framewok](https://github.com/pyfony/pyfony)\n\n## Installation\n\n```\n$ poetry add pyfony-core\n```\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
