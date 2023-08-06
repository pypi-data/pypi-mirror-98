# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['structconf']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'structconf',
    'version': '0.2.1',
    'description': 'struct config using yaml',
    'long_description': '# StructConf\n\n[![PyPI](https://img.shields.io/pypi/v/structconf?color=blue)](https://pypi.org/project/structconf/)\n\n\nConfig your project with yaml and validation\n\n',
    'author': 'Wenqi Zhao',
    'author_email': '1027572886a@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Green-Wood/structconf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
