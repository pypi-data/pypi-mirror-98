# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycache']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-cache',
    'version': '0.1.0',
    'description': 'Simple to use caching decorator with more capabilites than the default one.',
    'long_description': '# Method cache\n\nIf you want to cache the calls to a specific method or function you could use the python `functools.cache` decorator. If\nthis has not enough configuration options for your taste, or you work with arguments which are not hashable this cache\ndecorator could be useful.\n\n## Advantages\n\n+ Works with non hashable objects\n+ Set expiry after time\n+ Set expiry after a schedule\n+ Set maximal cache size per method\n+ Works with sync and async functions\n+ Properly tested\n\n## Usage\n\nUse a cache which expires after a certain amount of time:\n\n```python\nfrom pycache import cache\n\n\n# The format for expires_every is <hh:mm:ss>\n# This cache would expire every 10 seconds\n@cache(expires_every="*:*:10")\ndef please_cache():\n    pass\n\n\n# This cache would expire every 5 minutes and 10 seconds\n@cache(expires_every="*:5:10")\ndef please_cache():\n    pass\n```\n\nUse a cache which expires every time at a certain time (A bit like a cron job).\n\n```python\nfrom pycache import cache\n\n\n# The format for schedule is <hh:mm:ss>\n# This cache would expire every day at 15:10:05\n@cache(schedule="15:10:05")\ndef please_cache():\n    pass\n\n\n# This cache would expire every hour 8 minutes after a full hour\n@cache(schedule="*:08:00")\ndef please_cache():\n    pass\n```\n\nLimit the number of cache entries\n\n```python\nfrom pycache import cache\n\n\n# This would result in only one cache entry\n@cache(expires_every="*:*:10", max_cache_size=1)\ndef please_cache(data: str):\n    pass\n\n\n# Gets placed in cache\nplease_cache("hello")\n# Gets called from cache\nplease_cache("hello")\n\n# Gets placed in cache and "hello" gets removed\nplease_cache("world")\n\n# Is not found in cache, because "world" is the only cache entry, \n# because the cache size is one\nplease_cache("hello")\n```\n',
    'author': 'HuiiBuh',
    'author_email': None,
    'maintainer': 'HuiiBuh',
    'maintainer_email': None,
    'url': 'https://github.com/HuiiBuh/pycache',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
