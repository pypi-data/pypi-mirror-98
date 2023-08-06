# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plyder', 'plyder.routes', 'plyder.static', 'plyder.templates']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'aiofiles>=0.6.0,<0.7.0',
 'appdirs>=1.4.4,<2.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'jsonschema>=3.2.0,<4.0.0',
 'loguru>=0.5.3,<0.6.0',
 'mega.py>=1.0.8,<2.0.0',
 'sh>=1.14.1,<2.0.0',
 'uvicorn>=0.13.4,<0.14.0']

entry_points = \
{'console_scripts': ['plyder = plyder:main']}

setup_kwargs = {
    'name': 'plyder',
    'version': '0.2.0',
    'description': 'Download manager with web-interface.',
    'long_description': '# plyder\n\n[![PyPI](https://img.shields.io/pypi/v/plyder.svg?style=flat)](https://pypi.python.org/pypi/plyder)\n[![Tests](https://github.com/kpj/plyder/workflows/Tests/badge.svg)](https://github.com/kpj/plyder/actions)\n\nDownload manager with web-interface.\n\n\n## Installation\n\n```python\n$ pip install plyder\n```\n\n\n## Usage\n\n```bash\n$ plyder\n```\n\n`plyder` works out of the box. Though you might want to adapt the configuration to your taste.\n',
    'author': 'kpj',
    'author_email': 'kim.philipp.jablonski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kpj/plyder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
