# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsxmltojson']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.2,<5.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'awsxmltojson',
    'version': '0.1.0',
    'description': 'Converts XML Responses from AWS API to JSON',
    'long_description': None,
    'author': 'seveibar',
    'author_email': 'seveibar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
