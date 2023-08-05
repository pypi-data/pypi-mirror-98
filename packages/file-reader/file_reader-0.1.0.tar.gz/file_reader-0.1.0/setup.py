# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_reader', 'file_reader.hosts']

package_data = \
{'': ['*'], 'file_reader': ['assets/*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

extras_require = \
{'all': ['boto3>=1.16.0,<2.0.0',
         'smbprotocol>=1.2.0,<2.0.0',
         'paramiko>=2.7.2,<3.0.0',
         'pyarrow>=2.0.0,<3.0.0'],
 'hdfs': ['pyarrow>=2.0.0,<3.0.0'],
 's3': ['boto3>=1.16.0,<2.0.0'],
 'sftp': ['paramiko>=2.7.2,<3.0.0'],
 'smb': ['smbprotocol>=1.2.0,<2.0.0'],
 'ssh': ['paramiko>=2.7.2,<3.0.0']}

setup_kwargs = {
    'name': 'file-reader',
    'version': '0.1.0',
    'description': 'A tool for reading file from different sources with a single interface',
    'long_description': None,
    'author': 'Marc Rijken',
    'author_email': 'marc@rijken.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrijken/file_reader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
