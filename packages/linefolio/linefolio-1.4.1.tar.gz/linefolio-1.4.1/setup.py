# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linefolio', 'linefolio.tests']

package_data = \
{'': ['*'], 'linefolio': ['examples/*'], 'linefolio.tests': ['test_data/*']}

install_requires = \
['empyrical>=0.5.5,<0.6.0',
 'ipython>=7.21.0,<8.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pytz>=2021.1,<2022.0',
 'quantrocket-moonshot>=2.4.0,<3.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'scipy>=1.6.1,<2.0.0',
 'seaborn>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'linefolio',
    'version': '1.4.1',
    'description': 'Backtest performance analysis and charting for MoonLine, but with pyfolio.',
    'long_description': None,
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
