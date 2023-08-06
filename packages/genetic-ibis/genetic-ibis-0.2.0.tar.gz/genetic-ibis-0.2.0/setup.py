# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['ibis', 'ibis.datastucture', 'ibis.ingress', 'ibis.output', 'ibis.scoring']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'click>=7.1.2,<8.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'pytest>=6.2.2,<7.0.0',
 'rich>=9.11.0,<10.0.0',
 'scipy>=1.6.0,<2.0.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'genetic-ibis',
    'version': '0.2.0',
    'description': 'Genetic Circuit Scoring Algorithms',
    'long_description': None,
    'author': 'W.R. Jackson, Ben Bremer, Eric South',
    'author_email': None,
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
