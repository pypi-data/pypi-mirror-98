# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycache', 'pycache._cache']

package_data = \
{'': ['*'], 'pycache': ['_scheduler/*', '_shared/*']}

setup_kwargs = {
    'name': 'py-cache',
    'version': '0.2.0',
    'description': 'Simple to use caching decorator with more capabilites than the default one.',
    'long_description': '# Method _cache\n\n[![codecov](https://codecov.io/gh/HuiiBuh/pycache/branch/master/graph/badge.svg?token=WYBEMXAQVO)](https://codecov.io/gh/HuiiBuh/pycache)\n[![Upload Python Package](https://github.com/HuiiBuh/pycache/actions/workflows/publish.yml/badge.svg)](https://github.com/HuiiBuh/pycache/actions/workflows/publish.yml)\n\n## Why\n\nIf you want to _cache the calls to a specific method or function you could use the python `functools._cache` decorator.\nIf this has not enough configuration options for your taste, or you work with arguments which are not hashable this _\ncache decorator could be useful.\n\n## Advantages\n\n+ Works with non hashable objects\n+ Set expiry after time\n+ Set expiry after a schedule\n+ Set maximal _cache size per method\n+ Works with sync and async functions\n+ Properly tested\n\n## Usage\n\n### Cache\n\nUse a cache which expires after a certain amount of time:\n\n```python\nfrom pycache import cache\n\n\n# The format for schedule_type is <hh:mm:ss>\n# This _cache would expire every 10 seconds\n@cache(expires_at="*:*:10")\ndef please_cache():\n    pass\n\n\n# This _cache would expire every 5 minutes and 10 seconds\n@cache(expires_every="*:5:10")\ndef please_cache():\n    pass\n```\n\nUse a _cache which expires every time at a certain time (A bit like a cron job).\n\n```python\nfrom pycache import cache\n\n\n# The format for _schedule_str is <hh:mm:ss>\n# This _cache would expire every day at 15:10:05\n@cache(expires_at="15:10:05")\ndef please_cache():\n    pass\n\n\n# This _cache would expire every hour 8 minutes after a full hour\n@cache(expires_at="*:08:00")\ndef please_cache():\n    pass\n```\n\nLimit the number of _cache entries\n\n```python\nfrom pycache import cache\n\n\n# This would result in only one _cache entry\n@cache(expires_every="*:*:10", max_cache_size=1)\ndef please_cache(data: str):\n    pass\n\n\n# Gets placed in _cache\nplease_cache("hello")\n# Gets called from _cache\nplease_cache("hello")\n\n# Gets placed in _cache and "hello" gets removed\nplease_cache("world")\n\n# Is not found in _cache, because "world" is the only _cache entry, \n# because the _cache size is one\nplease_cache("hello")\n```\n\n### Schedule\n\n```python3\nfrom pycache import schedule, add_schedule, ScheduleSubscription\n\n\n# Gets called every 10 seconds\n@schedule(call_every="*:*:10")\ndef schedule_me():\n    pass\n\n\n# Gets called every at 10 am\n@schedule(call_every="10:00:00")\ndef schedule_me():\n    pass\n\n\n# Gets called 3 times\n@schedule(call_every="10:00:00", stop_after=3)\ndef schedule_me():\n    pass\n\n\n# Call with args and keyword args\n@schedule(call_every="10:00:00", args=(3,), kwargs={"hello": "world"})\ndef schedule_me(three: int, hello: str):\n    pass\n\n\ndef schedule_programmatically():\n    pass\n\n\n# Call this every five seconds\nschedule_subscription: ScheduleSubscription = add_schedule(schedule_programmatically, call_every="*:*:5")\n\n# Stop the schedule call\nschedule_subscription.stop()\n\n# Start the schedule again\nschedule_subscription.stop()\n```\n',
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
