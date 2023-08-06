# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arsene', 'arsene.connection', 'arsene.schemas']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0']

extras_require = \
{'redis': ['redis>=3.5.3,<4.0.0']}

setup_kwargs = {
    'name': 'arsene',
    'version': '0.1.6',
    'description': 'Easy data cache management',
    'long_description': '<p align="center">\n  <img width="320" height="320" src="https://github.com/JeremyAndress/arsene/blob/master/docs/arsene.png?raw=true" alt=\'Arsene\'>\n</p>\n\n<p align="center">\n<em>Simple cache management to make your life easy.</em>\n</p>\n\n<p align="center">\n<a href="https://github.com/JeremyAndress/arsene/actions/workflows/python-app.yml" target="_blank">\n    <img src="https://github.com/JeremyAndress/arsene/actions/workflows/python-app.yml/badge.svg" alt="Test">\n</a>\n\n<a href="LICENSE" target="_blank">\n    <img src="https://img.shields.io/github/license/peaceiris/actions-gh-pages.svg" alt="MIT">\n</a>\n\n<a href="https://pypi.python.org/pypi/arsene" target="_blank">\n    <img src="https://badge.fury.io/py/arsene.svg" alt="pypy">\n</a>\n</p>\n\n---\n\n### Requirements \n- Python 3.6+ \n\n### Installation\n```sh\npip install arsene\n```\n\n### Quick Start\nFor the tutorial, you must install redis as dependency\n\n```sh\npip install arsene[redis]\n```\n\n\nThe simplest Arsene setup looks like this:\n\n```python\nfrom datetime import datetime\nfrom arsene import Arsene, RedisModel\n\nredis = RedisModel(host=\'localhost\')\n\narsene = Arsene(redis_connection=redis)\n\n\n@arsene.cache(key=\'my_secret_key\', expire=2)\ndef get_user():\n    return {\n        \'username\': \'jak\',\n        \'last_session\': datetime(year=1999, month=2, day=3)\n    }\n\n\n# return and writes response to the cache\nget_user()\n\n# reads response to the cache\nget_user()\n# Response: {\'username\': \'jak\', \'last_session\': datetime.datetime(1999, 2, 3, 0, 0)}\n\n# reads response to the cache\narsene.get(key=\'my_secret_key\')\n\n# delete key to the cache\narsene.delete(key=\'my_secret_key\')\narsene.get(key=\'my_secret_key\')\n# Response: None\n\n```',
    'author': 'JeremyAndress',
    'author_email': 'jeremysilvasilva@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JeremyAndress/cobnut',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
