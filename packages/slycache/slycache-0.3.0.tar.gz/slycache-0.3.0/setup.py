# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slycache',
 'slycache.ext',
 'slycache.ext.django',
 'slycache.ext.flask',
 'tests',
 'tests.ext',
 'tests.ext.django',
 'tests.ext.flask']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9'],
 'django': ['Django>1.8'],
 'flask': ['Flask-Caching>=1.10.0,<2.0.0']}

setup_kwargs = {
    'name': 'slycache',
    'version': '0.3.0',
    'description': 'Service caching API',
    'long_description': '========\nslycache\n========\n\n\n.. image:: https://img.shields.io/pypi/v/slycache.svg\n        :target: https://pypi.python.org/pypi/slycache\n        :alt: PyPi version\n\n.. image:: https://img.shields.io/pypi/pyversions/slycache\n        :target: https://pypi.python.org/pypi/slycache\n        :alt: Python versions\n\n.. image:: https://github.com/snopoke/slycache/actions/workflows/ci.yml/badge.svg\n        :target: https://github.com/snopoke/slycache/actions/workflows/ci.yml\n        :alt: Build status\n\n.. image:: https://readthedocs.org/projects/slycache/badge/?version=latest\n        :target: https://slycache.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\nA caching API for python loosely modeled after the Java Caching API (JSR107_).\n\n.. _JSR107: https://docs.google.com/document/d/1YZ-lrH6nW871Vd9Z34Og_EqbX_kxxJi55UrSn4yL2Ak/edit\n\n\n* Documentation: https://slycache.readthedocs.io.\n\n.. note::\n    This library is in Alpha stage and not ready for production use.\n\nBasic Usage\n-----------\n\nStart by registering a cache backend:\n\n.. code:: python\n\n    slycache.register_backend("default", my_cache_backend)\n\nDefine a key namespace:\n\n.. code:: python\n\n    # define a key namespace\n    user_cache = slycache.with_defaults(namespace="user")\n\nUse the cache on methods and functions:\n\n.. code:: python\n\n    @user_cache.cache_result("{username}")\n    def get_user_by_username(username):\n        ...\n\n    @user_cache.cache_result("{user_id}")\n    def get_user_by_id(user_id):\n        ...\n\n    @user_cache.cache_put([\n        "{user.username}", "{user.user_id}"\n    ])\n    def save_user(user):\n        ...\n\n    @user_cache.cache_remove([\n        "{user.username}", "{user.user_id}"\n    ])\n    def delete_user(user):\n        ...\n\nFor more advanced usage see the documentation: https://slycache.readthedocs.io\n',
    'author': 'snopoke',
    'author_email': 'simongdkelly@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snopoke/slycache',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
