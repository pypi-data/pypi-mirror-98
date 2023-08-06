# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ssl_smtp_handler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ssl-smtp-handler',
    'version': '0.0.12',
    'description': 'A Python standard library logging handler which uses SMTP_SSL to send its mail ',
    'long_description': None,
    'author': 'Derek Wan',
    'author_email': 'd.wan@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
