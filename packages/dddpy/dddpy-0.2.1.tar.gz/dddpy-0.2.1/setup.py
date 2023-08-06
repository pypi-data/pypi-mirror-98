# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dddpy', 'dddpy.bases', 'dddpy.bases.common', 'dddpy.bases.domain']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=4.0.0,<7.0.0',
 'Inject>=4.3.1,<5.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'python-ulid>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'dddpy',
    'version': '0.2.1',
    'description': 'A framework to support ddd python projects',
    'long_description': '# dddpy\n[![CI](https://github.com/aeroworks-io/dddpy/workflows/CI/badge.svg)](https://github.com/aeroworks-io/dddpy/actions?query=workflow%3ACI)  \n[![codecov](https://codecov.io/gh/aeroworks-io/dddpy/branch/main/graph/badge.svg?token=BOO43Q8GIF)](https://codecov.io/gh/aeroworks-io/dddpy)\n\nA Framework to support ddd python projects\n',
    'author': 'Yuichiro Smith',
    'author_email': 'contact@yu-smith.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aeroworks-io/dddpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
