# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dicomrtai', 'dicomrtai.proto']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.36.1,<2.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['dicomrtai = dicomrtai.__main__:app']}

setup_kwargs = {
    'name': 'dicomrtai',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
