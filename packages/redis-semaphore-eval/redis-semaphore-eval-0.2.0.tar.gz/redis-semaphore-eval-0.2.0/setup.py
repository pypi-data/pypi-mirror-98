# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['redis_semaphore_eval']

package_data = \
{'': ['*']}

install_requires = \
['redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'redis-semaphore-eval',
    'version': '0.2.0',
    'description': 'A redis semaphore implementation using eval scripts',
    'long_description': '# Redis Semaphore Eval\n\n[![codecov](https://codecov.io/gh/wakemaster39/redis-semaphore-eval/branch/master/graph/badge.svg?token=BHTUPI4A0A)](https://codecov.io/gh/wakemaster39/redis-semaphore-eval)\n[![Actions Status](https://github.com/wakemaster39/redis-semaphore-eval/workflows/Tests/badge.svg)](https://github.comwakemaster39/redis-semaphore-eval/actions)\n[![Version](https://img.shields.io/pypi/v/redis-semaphore-eval)](https://pypi.org/project/redis-semaphore-eval/)\n[![PyPI - Wheel](https://img.shields.io/pypi/wheel/redis-semaphore-eval.svg)](https://pypi.org/project/redis-semaphore-eval/)\n[![Pyversions](https://img.shields.io/pypi/pyversions/redis-semaphore-eval.svg)](https://pypi.org/project/redis-semaphore-eval/)\n\nhttps://redislabs.com/ebook/part-2-core-concepts/chapter-6-application-components-in-redis/6-3-counting-semaphores/\n\n## Usage\nTo acquire a lock:\n```python\nfrom redis import Redis\nfrom redis_semaphore_eval import semaphore\n\nredis = Redis(host="localhost", port=6379, db=0)\nkey = "unique_lock_key"\nwith semaphore(redis, key=key, limit=2, expire_in=5, timeout=1) as lock_id:\n    ...\n```\n\nTo acquire a lock but continuously renew it in a background thread:\n```python\nfrom redis import Redis\nfrom redis_semaphore_eval import auto_renewing_semaphore\n\nredis = Redis(host="localhost", port=6379, db=0)\nkey = "unique_lock_key"\nwith auto_renewing_semaphore(\n    redis,\n    key=key,\n    limit=2,\n    expire_in=5,\n    timeout=1,\n    auto_renewal_interval=4\n) as lock_id:\n    ...\n```\n\n\n\n## Contributing\n\n```bash\npoetry run pre-commit install -t pre-commit -t commit-msg && poetry run pre-commit run --all\ndocker-compose up -d\npoetry run python -m pytest\ndocker-compose down\n```\n',
    'author': 'Cameron HUrst',
    'author_email': 'cameron.a.hurst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wakemaster39/redis-semaphore-eval',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
