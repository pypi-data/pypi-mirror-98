# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['litecow', 'litecow.common']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.33.2,<2.0.0', 'numpy>=1.17.4,<2.0.0', 'protobuf']

extras_require = \
{'server-cpu': ['onnxruntime>=1.7.0,<2.0.0', 'boto3>=1.11.14,<2.0.0'],
 'server-gpu': ['onnxruntime-gpu>=1.7.0,<2.0.0', 'boto3>=1.11.14,<2.0.0']}

entry_points = \
{'console_scripts': ['litecow-service = litecow.server:main']}

setup_kwargs = {
    'name': 'litecow',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Striveworks',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
