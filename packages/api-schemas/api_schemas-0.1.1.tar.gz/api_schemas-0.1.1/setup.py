# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api_schemas']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'api-schemas',
    'version': '0.1.1',
    'description': 'Create an intermediate representation of an api schema, that can be used to generate code.',
    'long_description': '# API schemas\n\nCreate an intermediate representation of an api schema, that can be used to generate code.\n\n**Example API schema**\n```\ntypedef object MyData\n    name: str\n    ?an_enum: {SUCCESS, FAILURE} Status # Optional enum \n    an_array[]: object People\n        name: str   # comments are also possible\n        *: str  # wildcards allow any string as key\n\nserver = http://localhost:5000/api/v1\n\npeople\n    uri: /people/<name>\n    GET\n        ->\n        <-\n            200\n                data: $MyData\n            404\n                err_msg: str\n            500\n                err_msg: str\n\n```',
    'author': 'JulianSobott',
    'author_email': 'julian.sobott@deutschebahn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
