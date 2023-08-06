# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xwire',
 'xwire.rest',
 'xwire.rest._private',
 'xwire.rest._private.proxy',
 'xwire.rest._private.proxy.decorators',
 'xwire.rest.public']

package_data = \
{'': ['*']}

install_requires = \
['pytest-mock>=3.5.1,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'xwire.common>=0.1.1,<0.2.0',
 'xwire.transport>=0.1.9,<0.2.0']

setup_kwargs = {
    'name': 'xwire.rest',
    'version': '0.1.11',
    'description': '',
    'long_description': None,
    'author': 'tylerlaberge',
    'author_email': 'tylerlaberge@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
