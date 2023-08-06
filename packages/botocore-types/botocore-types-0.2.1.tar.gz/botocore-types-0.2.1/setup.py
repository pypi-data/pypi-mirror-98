# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['botocore-stubs']

package_data = \
{'': ['*'], 'botocore-stubs': ['retries/*']}

setup_kwargs = {
    'name': 'botocore-types',
    'version': '0.2.1',
    'description': 'Type stubs for botocore',
    'long_description': "# botocore-types [![PyPI](https://img.shields.io/pypi/v/botocore-types.svg)](https://pypi.org/project/botocore-types/)\n\nType stubs for [`botocore`][0].\n\nFor boto3 stubs checkout [`mypy_boto3_builder`][1].\n\n## dev\n\n```sh\ns/lint\n```\n\n### publish new version\n\n1. increment version in `pyproject.toml`\n2. update `CHANGELOG.md`\n3. publish to pypi\n\n   ```\n   poetry publish --build\n   ```\n\n## generating stubs\n\n1. stubgen\n\n2. delete the `docs` folder as that's internal\n\n3. replace vendored imports with normal package imports. Don't want to have\n   to type `requests` when types for it already exist in `typeshed`.\n\n[0]: https://github.com/boto/botocore\n[1]: https://github.com/vemel/mypy_boto3_builder\n",
    'author': 'Steve Dignam',
    'author_email': 'steve@dignam.xyz',
    'url': 'https://github.com/sbdchd/botocore-types',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
