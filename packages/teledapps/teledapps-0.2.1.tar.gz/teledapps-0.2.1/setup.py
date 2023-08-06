# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teledapps',
 'teledapps.platform',
 'teledapps.platform.helpers',
 'teledapps.tokenlists',
 'teledapps.utils']

package_data = \
{'': ['*'], 'teledapps.tokenlists': ['lists/*']}

install_requires = \
['attrdict>=2.0.1,<3.0.0',
 'python-telegram-bot>=13.3,<14.0',
 'web3>=5.17.0,<6.0.0']

setup_kwargs = {
    'name': 'teledapps',
    'version': '0.2.1',
    'description': 'Python package for building Telegram bots, compatible with Teledapps',
    'long_description': None,
    'author': 'Sergey P',
    'author_email': 'pavlovdog.moscow@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
