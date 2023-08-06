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
    'version': '1.0.1',
    'description': 'A standard library compatible logging handler which sends mail via SMTP_SSL',
    'long_description': None,
    'author': 'Derek Wan',
    'author_email': 'd.wan@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dycw/ssl-smtp-handler',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
