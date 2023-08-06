# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['litecow_models']

package_data = \
{'': ['*']}

install_requires = \
['boto3-stubs>=1.17.23.0,<2.0.0.0',
 'boto3>=1.17.23,<2.0.0',
 'click',
 'mypy-boto3-s3>=1.17.23.0,<2.0.0.0',
 'onnxruntime>=1.7.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'torch>=1.7.0,<2.0.0',
 'tqdm>=4.59.0,<5.0.0',
 'urllib3>=1.26.3,<2.0.0']

entry_points = \
{'console_scripts': ['litecow = litecow_models.cli:cli']}

setup_kwargs = {
    'name': 'litecow-models',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Julian Medina',
    'author_email': 'jmedina@striveworks.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
