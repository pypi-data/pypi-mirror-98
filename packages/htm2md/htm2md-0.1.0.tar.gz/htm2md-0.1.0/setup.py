# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htm2md']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'htm2md',
    'version': '0.1.0',
    'description': 'convert html to markdown',
    'long_description': '======\nhtm2md\n======\n\nhtm2md is a Python library to convert html to markdown.\n\nInstallation\n============\n\n.. sourcecode::\n\n  pip install htm2md\n\n\nUsage\n=====\n\n.. sourcecode:: python\n\n  import htm2md\n\n  # convert html to markdown\n  md = htm2md.convert("<p>This is an <a href=\'https://example.com\'>example</a>.</p>")\n  \n  # output: This is an [example](https://example.com).\n  print(md)\n\nLicense\n=======\n\n`MIT <https://choosealicense.com/licenses/mit/>`_\n',
    'author': 'miso',
    'author_email': 'green-24@outlook.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miso24',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
