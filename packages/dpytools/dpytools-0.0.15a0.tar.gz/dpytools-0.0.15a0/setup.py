# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dpytools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dpytools',
    'version': '0.0.15a0',
    'description': 'Simple tools to build discord bots using discord.py',
    'long_description': "# dpytools\nToolset to speed up developing discord bots using discord.py\n\n<hr>\n\n## Status of the project\n\nEarly development. As such it's expected to be unstable and unsuited for production.\n\nAll the presented tools have stringdocs.\n\n# Contributing\nFeel free to make a pull request.",
    'author': 'chrisdewa',
    'author_email': 'alexdewa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrisdewa/dpytools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
