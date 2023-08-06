# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepl_grpc']

package_data = \
{'': ['*']}

install_requires = \
['deepl-scraper-pp>=0.1.1,<0.2.0',
 'grpcio>=1.36.1,<2.0.0',
 'logzero>=1.6.3,<2.0.0',
 'portalocker>=2.2.1,<3.0.0']

setup_kwargs = {
    'name': 'deepl-grpc',
    'version': '0.1.0',
    'description': 'deepl grpc server and client',
    'long_description': '# deepl-grpc\n[![tests](https://github.com/ffreemt/deepl-grpc/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-grpc.svg)](https://badge.fury.io/py/deepl-grpc)\n\ndeepl grpc, server and client, cross platform (Windows/MacOS/Linux) \n\n## Installation\n*   Install ``grpc-reflection``\n    *   ``grpc-reflection`` cannot be installed using `poetry add`. Use ``pip install grpc-reflection`` instead.\n*   Install the rest as usual\n```bash\npip install deepl-grpc\n```\nor\n```bash\npoetry add deepl-grpc\n```\n\nor clone the repo and install from it.\n\n## Usage\n\n### Interactive\n\n*   [Optional] Start the grpc server\n```python\npython -m deepl_grpc.deepl_server\n```\n\n*   Start the client\n```python\npython -m deepl_grpc.deepl_client  # to chinese\n\n# python -m deepl_grpc.deepl_client de  # to german\n```\n\n### WebUI\nDownload `grpcui` and run, for example in Windows\n```bash\ngrpcui.exe -plaintext 127.0.0.1:50051\n```\nto explore the server in the same manner as Postman for REST.\n\n### More coming soon\n',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/deepl-grpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
