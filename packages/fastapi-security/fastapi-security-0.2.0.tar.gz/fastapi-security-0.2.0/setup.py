# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_security']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT[crypto]>=2,<3', 'aiohttp>=3,<4', 'fastapi>=0,<1', 'pydantic>=1,<2']

setup_kwargs = {
    'name': 'fastapi-security',
    'version': '0.2.0',
    'description': 'Add authentication and authorization to your FastAPI app via dependencies.',
    'long_description': '# FastAPI Security\n\n[![Continuous Integration Status](https://github.com/jmagnusson/fastapi-security/actions/workflows/ci.yml/badge.svg?event=push)](https://github.com/jmagnusson/fastapi-security/actions/workflows/ci.yml)\n[![Continuous Delivery Status](https://github.com/jmagnusson/fastapi-security/actions/workflows/cd.yml/badge.svg?event=push)](https://github.com/jmagnusson/fastapi-security/actions/workflows/cd.yml)\n[![Python Versions](https://img.shields.io/pypi/pyversions/fastapi-security.svg)](https://pypi.org/project/fastapi-security/)\n[![Code Coverage](https://img.shields.io/codecov/c/github/jmagnusson/fastapi-security?color=%2334D058)](https://codecov.io/gh/jmagnusson/fastapi-security)\n[![PyPI Package](https://img.shields.io/pypi/v/fastapi-security?color=%2334D058&label=pypi%20package)](https://pypi.org/project/fastapi-security)\n\nAdd authentication and authorization to your FastAPI app via dependencies.\n\n## Features\n\n- Authentication via JWT-based OAuth 2 access tokens and via Basic Auth\n- Pydantic-based `User` model for authenticated and anonymous users\n- Sub-classable `UserPermission` dependency to check against the `permissions` attribute returned in OAuth 2 access tokens\n- Able to extract user info from access tokens via OpenID Connect\n\n## Limitations\n\n- Only supports validating access tokens using public keys from a JSON Web Key Set (JWKS) endpoint. I.e. for use with external identity providers such as Auth0 and ORY Hydra.\n- Permissions can only be picked up automatically from OAuth2 tokens, from the non-standard `permissions` list attribute (Auth0 provides this, maybe other identity providers as well). For all other use cases, `permission_overrides` must be used. For example if there\'s a basic auth user called `user1` you can set `permission_overrides={"user1": ["*"]}` to give the user access to all permissions, or `permission_overrides={"user1": ["products:create"]}` to only assign `user1` with the permission `products:create`.\n\n\n## Installation\n\n```bash\npip install fastapi-security\n```\n\n## Usage examples\n\nExamples on how to use [can be found here](/examples).\n\n## TODO\n\n- Write more tests\n',
    'author': 'Jacob Magnusson',
    'author_email': 'm@jacobian.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmagnusson/fastapi-security',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
