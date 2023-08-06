# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['truhanen', 'truhanen.windowlayouts']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'dataclasses-json>=0.5.2,<0.6.0']

extras_require = \
{'pandas': ['pandas>=1.2.3,<2.0.0']}

entry_points = \
{'console_scripts': ['windowlayouts = truhanen.windowlayouts:main']}

setup_kwargs = {
    'name': 'truhanen.windowlayouts',
    'version': '0.2.0',
    'description': 'Store & restore window layouts on the X window system',
    'long_description': None,
    'author': 'Tuukka Ruhanen',
    'author_email': 'tuukka.t.ruhanen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
