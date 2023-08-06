# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['get_ppbrowser']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.6.3,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'pyppeteer2>=0.2.2,<0.3.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'python-dotenv>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'get-ppbrowser',
    'version': '0.1.2',
    'description': 'Create a valid pyppeteer browser',
    'long_description': '# get-ppbrowser\n[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![build-and-pytest](https://github.com/ffreemt/get-ppbrowser/actions/workflows/build-and-pytest.yml/badge.svg)](https://github.com/ffreemt/get-ppbrowser/actions/workflows/build-and-pytest.yml)[![CodeQL](https://github.com/ffreemt/get-ppbrowser/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/ffreemt/get-ppbrowser/actions/workflows/codeql-analysis.yml)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/get-ppbrowser.svg)](https://badge.fury.io/py/get-ppbrowser)\n\nInstantiate a pyppeteer browser object.\n\n## Instalation\n```bash\npip install get-ppbrowser\n# pip  install get-ppbrowser -U  # to upgrade\n```\nor\n```bash\npoetry add get-ppbrowser\n# poetry add get-ppbrowser@latest  # to upgrade\n```\n\n## Usage\n```python\nfrom get_ppbrowser import get_ppbrowser\n\nbrowser = await get_ppbrowser()\npage = await browser.newPage()\nawait page.goto("http://www.example.com")\n```\n\n### PPBROWSER_HEADFUL, PPBROWSER_DEBUG, PPBROWSER_PROXY\nEnvironment variables can be set with, for example, in Windows\n\n```bash\nset PPBROWSER_HEADFUL=1\n```\n\nor in Linux/iOS\n```bash\nexport PPBROWSER_HEADFUL=1\n```\nor in `python`\n\n```python\nimport os\n\nos.environ["PPBROWSER_HEADFUL"] = "1"\n```\n',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/get-ppbrowser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
