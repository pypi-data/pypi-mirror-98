# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kit', 'kit.torch']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['hydra-core==1.1.0.dev4']

setup_kwargs = {
    'name': 'palkit',
    'version': '0.1.4',
    'description': 'Useful functions.',
    'long_description': '# PAL kit\n\nThis is a collection of useful functions for code that we write in our group.\n\n## Install\n\nRun\n```\npip install palkit\n```\n\nor install directly from GitHub:\n```\npip install git+https://github.com/predictive-analytics-lab/palkit.git\n```\n',
    'author': 'PAL',
    'author_email': 'info@predictive-analytics-lab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/predictive-analytics-lab/palkit',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
