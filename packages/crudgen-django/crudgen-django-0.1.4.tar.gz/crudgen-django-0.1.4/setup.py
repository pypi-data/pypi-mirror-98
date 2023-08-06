# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crudgen_django', 'crudgen_django.console', 'crudgen_django.hacks']

package_data = \
{'': ['*']}

install_requires = \
['Django<3.0',
 'crudgen>=0.1.1,<0.2.0',
 'djangorestframework>=3.12.2,<4.0.0',
 'drf-extensions>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['generate = crudgen_django.console.generate:main']}

setup_kwargs = {
    'name': 'crudgen-django',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'pouria',
    'author_email': 'pooriazmn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
