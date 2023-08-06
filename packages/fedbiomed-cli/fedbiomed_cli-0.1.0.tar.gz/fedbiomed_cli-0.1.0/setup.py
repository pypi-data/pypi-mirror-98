# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fedbiomed_cli', 'fedbiomed_cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.14,<4.0.0',
 'paho-mqtt>=1.5.1,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'persist-queue>=0.5.1,<0.6.0',
 'requests>=2.25.1,<3.0.0',
 'tinydb>=4.4.0,<5.0.0',
 'torch>=1.8.0,<2.0.0',
 'torchvision>=0.9.0,<0.10.0',
 'validators>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'fedbiomed-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Santiago SILVA',
    'author_email': '16252054+sssilvar@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
