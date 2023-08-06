# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepl_grpc']

package_data = \
{'': ['*']}

install_requires = \
['deepl-scraper-pp>=0.1.1,<0.2.0',
 'google>=3.0.0,<4.0.0',
 'grpcio-reflection>=1.36.1,<2.0.0',
 'grpcio-tools>=1.36.1,<2.0.0',
 'grpcio>=1.36.1,<2.0.0',
 'logzero>=1.6.3,<2.0.0',
 'portalocker>=2.2.1,<3.0.0',
 'pysocks>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'deepl-grpc',
    'version': '0.1.1',
    'description': 'deepl grpc server and client',
    'long_description': '# deepl-grpc\n[![tests](https://github.com/ffreemt/deepl-grpc/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-grpc.svg)](https://badge.fury.io/py/deepl-grpc)\n\ndeepl grpc, server and client, cross platform (Windows/MacOS/Linux)\n\n## Installation\n*   Install ``grpcio-reflection``\n    *   ``grpc-reflection`` cannot be installed using `poetry add`. Use ``pip install grpcio-reflection`` instead.\n*   Install the rest as usual\n```bash\npip install deepl-grpc\n```\nor\n```bash\npoetry add deepl-grpc\n```\n\nor clone the repo (`git clone https://github.com/ffreemt/deepl-grpc.git`) and install from it. For example\n```python\ngit clone https://github.com/ffreemt/deepl-grpc.git\ncd deepl-grpc\npython3.8 -m venv .venv  # require python3.7+\n\n# for Linux/MacOS, you\'d need to install venv and dev if you haven\'t done so\n# sudo apt install python3.8-venv\n# sudo apt install python3.8-dev\n\nsource .venv/bin/activate  # or in Windows do: .venv\\Scripts\\activate\n\npip install grpcio-reflection\n\npip install -r requirements.txt\n# or poetry install --no-dev\n\npython -m deepl_grpc.deepl_client\n\n```\n\n## Usage\n\n### `python` code\n```python\nfrom deepl_grpc.deepl_client import DeeplClient\nfrom linetimer import CodeTimer\n\nclient = DeeplClient()\n\ntext = "test this and that"\nwith CodeTimer(unit="s"):\n    result = client.get_url(message=text)\n# Code block took: 1.99860 s\n\nprint(result.message)\n# 试探 左右逢源 检验 审时度势\n\nto_lang = "de"\nwith CodeTimer(unit="s"):\n  result = client.get_url(message=text, to_lang=to_lang,)\n# Code block took: 2.02847 s\n\nprint(result.message)\n# "Testen Sie dieses und jenes a Testen Sie dies und das a testen Sie dies und das Testen Sie dieses und jenes"\n\n```\n\n### Interactive\n\n*   Start the grpc server\n```python\npython -m deepl_grpc.deepl_server\n```\nThe first run in Linux may take a while since `chromium` (~1G) needs to be downloaded. In Windows, Chrome will be used if it\'s available.\n\n*   Start the client\n```python\npython -m deepl_grpc.deepl_client  # to chinese\n\n# python -m deepl_grpc.deepl_client de  # to german\n```\n\n### WebUI\nDownload `grpcui` and run, for example in Windows\n```bash\ngrpcui.exe -plaintext 127.0.0.1:50051\n```\nto explore the server in the same manner as Postman for REST.\n\n### pyppeteer issues in Linux\nYou may encounter the following error in Linux:\n\n **chromium/linux-588429/chrome-linux/chrome**: error while loading shared libraries: libX11-xcb.so.1: cannot open shared object file: No such file or directory\n\nYou may wish to try this fix in Ubuntu [https://medium.com/@cloverinks/how-to-fix-puppetteer-error-ibx11-xcb-so-1-on-ubuntu-152c336368](https://medium.com/@cloverinks/how-to-fix-puppetteer-error-ibx11-xcb-so-1-on-ubuntu-152c336368)\n```bash\nsudo apt-get install gconf-service libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxss1 libxtst6 libappindicator1 libnss3 libasound2 libatk1.0-0 libc6 ca-certificates fonts-liberation lsb-release xdg-utils wget\n```\n\n### More coming soon\n\n<!---\nhttps://www.cnblogs.com/lsdb/p/12102418.html\n17     # portalocker.lock(file, portalocker.constants.LOCK_EX)\n18     portalocker.lock(file, portalocker.LOCK_EX | portalocker.LOCK_NB)\n\nimport sys\nfrom pathlib import Path\n\n_ = Path(__file__).absolute().parent.parent.as_posix()\nsys.path.append(_)\n\n\nworkingDir = Path(__file__).absolute().parent.as_posix()\n\ncmd = f"nohup python {workingDir}/deepl_server.py >/dev/null 2>&1 &"\n\nfullpath = "/tmp"\ncmd = f"nohup python {fullpath}/file.py > {fullpath}/out 2>&1 &"\nsubprocess.Popen(cmd, shell=True)\n\nsubprocess.Popen("pythonw file.py", shell=True)\n\n--->',
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
