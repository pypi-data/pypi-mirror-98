# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patlib']

package_data = \
{'': ['*']}

install_requires = \
['ipdb', 'ipython', 'jedi<0.18', 'line_profiler', 'pudb', 'see']

extras_require = \
{'math': ['matplotlib', 'pyqt5==5.15.2', 'scipy', 'numpy>=1.20.1,<2.0.0'],
 'misc': ['pyyaml', 'toml', 'tabulate', 'tqdm']}

setup_kwargs = {
    'name': 'patlib',
    'version': '0.2.6',
    'description': 'A collection of tools.',
    'long_description': '# patlib\n\nA collection of tools developed in conjunction with DAPPER.\n',
    'author': 'patricknraanes',
    'author_email': 'patrick.n.raanes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
