# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anime_dl', 'anime_dl.scraper']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'colorama>=0.4.4,<0.5.0',
 'requests>=2.25.1,<3.0.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['anime-dl = anime_dl.main:main']}

setup_kwargs = {
    'name': 'anime-dl',
    'version': '0.1.0',
    'description': 'A simple command-line tool to download anime.',
    'long_description': '# anime-dl\n\nA simple command line tool written in python to download anime.\n\n## Installation\n\n```sh\n$ pip install anime-dl\n```\n\n## Usage\n\n```\nusage: anime-dl [-h] [-v] -s KEYWORD\n\nA simple command-line tool to download anime.\n\noptional arguments:\n  -h, --help                    show this help message and exit\n  -v, --version                 display the version and exit\n  -s KEYWORD, --search KEYWORD  search for an anime\n```\n\n## License\n\nDistributed under the MIT License. See [LICENSE](LICENSE)  for more information.\n\n[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)',
    'author': 'Rohan Kumar',
    'author_email': 'rohankmr414@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rohankmr414/anime_dl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
