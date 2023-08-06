# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bme280spi']

package_data = \
{'': ['*']}

install_requires = \
['spidev>=3.5,<4.0']

entry_points = \
{'console_scripts': ['bme280spi = bme280spi.__main__:main']}

setup_kwargs = {
    'name': 'bme280spi',
    'version': '0.1.0',
    'description': 'Library for BME280 sensor through spidev',
    'long_description': '# bme280spi\nLibrary for BME280 sensor through spidev\n',
    'author': 'Kuzj',
    'author_email': 'kuzj99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kuzj/bme280spi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
