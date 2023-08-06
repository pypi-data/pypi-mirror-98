# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kerochan', 'kerochan.import']

package_data = \
{'': ['*']}

install_requires = \
['inquirer>=2.7.0,<3.0.0',
 'parse>=1.18.0,<2.0.0',
 'psutil>=5.8.0,<6.0.0',
 'tqdm>=4.55.1,<5.0.0']

entry_points = \
{'console_scripts': ['kerochan_import = kerochan.import.__main__:__main__']}

setup_kwargs = {
    'name': 'kerochan',
    'version': '0.1.0',
    'description': 'Kero-chan is a tool to help you collect your pictures from your camera',
    'long_description': None,
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
