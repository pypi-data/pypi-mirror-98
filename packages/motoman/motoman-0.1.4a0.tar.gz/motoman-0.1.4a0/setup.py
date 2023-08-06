# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['motoman', 'motoman.commands', 'motoman.commands.devices']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.8.1,<3.0.0',
 'colorama>=0.4.4,<0.5.0',
 'prompt-toolkit>=3.0.17,<4.0.0',
 'pyserial>=3.5,<4.0',
 'python-nubia>=0.2b5,<0.3']

entry_points = \
{'console_scripts': ['motoman = motoman.entry:main']}

setup_kwargs = {
    'name': 'motoman',
    'version': '0.1.4a0',
    'description': 'A command line tool to control a set of stepper motors',
    'long_description': '# motoman\n***Moto***rs ***Man***ager CLI\n\n\n[![Tests](https://github.com/TechnocultureResearch/MotorsManager-CLI/actions/workflows/python-package.yml/badge.svg?branch=dev)](https://github.com/TechnocultureResearch/MotorsManager-CLI/actions/workflows/python-package.yml)\n\nA command line tool to control a set of stepper motors. Intended to serve the specific needs of Microfabricator T.\n\n# Usage\n<img width="645" alt="Screenshot 2021-03-15 at 2 27 23 AM" src="https://user-images.githubusercontent.com/33483920/111083938-1dd29400-8536-11eb-99e8-800182b5d991.png">\n\n## On Linux, MacOS\n```bash\nmotoman\n```\n\n## On Windows\n```cmd\npy -m motoman.entry\n```\n\n# Install\n\n## Requirements\n- Python 3.7 (or later)\n- pip\n\n## On Linux, MacOS\n```bash\npip install motoman\n```\n\n## On Windows\n```cmd\npy -m pip install motoman\n```\n\nor, \n\n```bash\npip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple motoman\n```\n\n# More on Usage\n## verbose mode\n```bash\nmotoman -v\n```\n',
    'author': 'Satyam Tiwary',
    'author_email': 'satyamtiwary@vvbiotech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://www.technocultureresearch.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
