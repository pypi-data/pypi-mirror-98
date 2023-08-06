# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfdtools', 'cfdtools.ic3', 'cfdtools.meshbase', 'cfdtools.physics']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.15,<2.0']

setup_kwargs = {
    'name': 'cfdtools',
    'version': '0.0.1',
    'description': 'Tools for mesh and solution management in CFD',
    'long_description': None,
    'author': 'j.gressier',
    'author_email': 'jeremie.gressier@isae-supaero.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jgressier/cfdtools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
