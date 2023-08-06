# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fettler']

package_data = \
{'': ['*']}

install_requires = \
['aioredis', 'asyncmy', 'ciso8601', 'click', 'dynaconf', 'loguru']

entry_points = \
{'console_scripts': ['fettler = fettler.cli:main']}

setup_kwargs = {
    'name': 'fettler',
    'version': '0.1.0',
    'description': 'Auto refresh cache of redis with MySQL binlog',
    'long_description': '# Fettler\n\n[![image](https://img.shields.io/pypi/v/fettler.svg?style=flat)](https://pypi.python.org/pypi/fettler)\n[![image](https://img.shields.io/github/license/long2ice/fettler)](https://github.com/long2ice/fettler)\n[![pypi](https://github.com/long2ice/fettler/actions/workflows/pypi.yml/badge.svg)](https://github.com/long2ice/fettler/actions/workflows/pypi.yml)\n[![ci](https://github.com/long2ice/fettler/actions/workflows/ci.yml/badge.svg)](https://github.com/long2ice/fettler/actions/workflows/ci.yml)\n\n## Introduction\n\n`Fettler` is a service that help you refresh redis cache automatically. By listening on MySQL binlog, you can refresh\nredis cache in a timely manner and devoid of sensation or consciousness.\n\n![architecture](./images/architecture.png)\n\n## Install\n\nJust install from pypi:\n\n```shell\n> pip install fettler\n```\n\n## Usage\n\n### Config file\n\nThe example can be found in [config.yml](./config.yml).\n\n### Run services\n\nFirst you should run the services, which include `producer`, `consumer`.\n\n#### Use `docker-compose`(recommended)\n\n```shell\ndocker-compose up -d --build\n```\n\nThen the services is running.\n\n#### Run manual\n\n##### Run producer\n\nThe producer listens on MySQL binlog and send data changes to redis message queue.\n\n```shell\n> fettler produce\n```\n\n##### Run consumer\n\nThe consumer consume message queue and delete invalid caches by data changes and refresh policy registered from server.\n\n```shell\n> fettler consume\n```\n\n## Register cache refresh policy\n\nSee [examples](./examples) to see how to add cache refresh policy in you application.\n\n## License\n\nThis project is licensed under the [Apache-2.0](./LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/fettler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
