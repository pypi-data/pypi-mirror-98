# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seminar',
 'seminar.apis',
 'seminar.commands',
 'seminar.models',
 'seminar.utils']

package_data = \
{'': ['*'],
 'seminar': ['templates/*',
             'templates/group/*',
             'templates/kaggle/*',
             'templates/notebooks/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'Pygments>=2.7.3,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'docker>=4.4.1,<5.0.0',
 'emoji>=0.6.0,<0.7.0',
 'jupyter>=1.0.0,<2.0.0',
 'kaggle>=1.5.10,<2.0.0',
 'nbconvert>=6.0.7,<7.0.0',
 'nbformat>=5.0.8,<6.0.0',
 'nbgrader>=0.6.1,<0.7.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'pandoc>=1.0.2,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['seminar = seminar.cli:seminar']}

setup_kwargs = {
    'name': 'seminar-toolkit',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'John Muchovej',
    'author_email': 'muchovej@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
