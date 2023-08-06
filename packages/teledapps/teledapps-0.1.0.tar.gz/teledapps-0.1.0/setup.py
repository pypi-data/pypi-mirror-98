# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teledapps', 'teledapps.platform']

package_data = \
{'': ['*']}

install_requires = \
['python-telegram-bot>=13.3,<14.0']

setup_kwargs = {
    'name': 'teledapps',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sergey P',
    'author_email': 'pavlovdog.moscow@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
