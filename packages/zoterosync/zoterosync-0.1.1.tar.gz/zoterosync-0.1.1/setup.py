# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['zoterosync']
install_requires = \
['click>=7.1.2,<8.0.0',
 'pybtex>=0.24.0,<0.25.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'python-rclone>=0.0.2,<0.0.3']

setup_kwargs = {
    'name': 'zoterosync',
    'version': '0.1.1',
    'description': 'Syncs local zotero files to a remote storage using rclone. This is a work in progress.',
    'long_description': None,
    'author': 'Marcelo Akira Inuzuka',
    'author_email': 'marceloakira@ufg.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3',
}


setup(**setup_kwargs)
