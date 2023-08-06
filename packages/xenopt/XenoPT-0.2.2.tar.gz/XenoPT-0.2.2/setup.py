# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xenopt']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'xenopt',
    'version': '0.2.2',
    'description': 'A collection of published thermobarometers for garnet two-pyroxene xenoliths. Allows for input of .csv data, with template provided in tb_parameters.py',
    'long_description': '# XenoPT\nGarnet two-pyroxene thermobarometry package.\n\nhttps://pypi.org/project/xenopt/\n',
    'author': 'Khalil Droubi',
    'author_email': 'droubi@wisc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/okdpetrology/XenoPT',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
