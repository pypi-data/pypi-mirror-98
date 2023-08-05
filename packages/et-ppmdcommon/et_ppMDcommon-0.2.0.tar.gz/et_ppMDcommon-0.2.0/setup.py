# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['et_ppmdcommon']
install_requires = \
['et-micc-build>=1.0.20,<2.0.0', 'numpy>=1.20.1,<2.0.0']

setup_kwargs = {
    'name': 'et-ppmdcommon',
    'version': '0.2.0',
    'description': '<Enter a one-sentence description of this project here.>',
    'long_description': '=============\net_ppMDcommon\n=============\n\nCommon components for the Parallel Programming project assignement 2021\n\n* Free software: MIT license\n\n',
    'author': 'Bert Tijskens',
    'author_email': 'engelbert.tijskens@uantwerpen.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etijskens/et_ppMDcommon',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
