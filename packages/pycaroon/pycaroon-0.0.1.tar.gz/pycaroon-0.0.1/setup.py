# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycaroon']

package_data = \
{'': ['*']}

install_requires = \
['pyglet>=1.5.15,<2.0.0']

setup_kwargs = {
    'name': 'pycaroon',
    'version': '0.0.1',
    'description': 'Secret',
    'long_description': None,
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
