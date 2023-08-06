# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s2py']

package_data = \
{'': ['*']}

install_requires = \
['fake-useragent>=0.1.11,<0.2.0',
 'httpx>=0.17.0,<0.18.0',
 'parsel>=1.6.0,<2.0.0',
 'rapidfuzz>=1.2.1,<2.0.0',
 'selenium>=3.141.0,<4.0.0',
 'webdriver-manager>=3.3.0,<4.0.0',
 'whoswho>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 's2py',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'reiyw',
    'author_email': 'reiyw.setuve@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
