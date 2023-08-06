# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['musamusa_atext']

package_data = \
{'': ['*']}

install_requires = \
['musamusa-errors>=0.0.9,<0.0.10']

setup_kwargs = {
    'name': 'musamusa-atext',
    'version': '0.0.1',
    'description': 'MusaMusa::AnnotatedText',
    'long_description': None,
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
