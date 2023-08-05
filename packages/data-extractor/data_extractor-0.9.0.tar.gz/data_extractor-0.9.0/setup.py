# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_extractor']

package_data = \
{'': ['*']}

extras_require = \
{'cssselect': ['lxml>=4.3.0,<5.0.0', 'cssselect>=1.0.3,<2.0.0'],
 'docs': ['lxml>=4.3.0,<5.0.0',
          'cssselect>=1.0.3,<2.0.0',
          'jsonpath-rw>=1.4.0,<2.0.0',
          'jsonpath-rw-ext>=1.2,<2.0',
          'jsonpath-extractor>=0.5.0,<0.8',
          'sphinx>=2.2,<3.0'],
 'jsonpath-extractor': ['jsonpath-extractor>=0.5.0,<0.8'],
 'jsonpath-rw': ['jsonpath-rw>=1.4.0,<2.0.0'],
 'jsonpath-rw-ext': ['jsonpath-rw>=1.4.0,<2.0.0', 'jsonpath-rw-ext>=1.2,<2.0'],
 'lint': ['lxml>=4.3.0,<5.0.0',
          'cssselect>=1.0.3,<2.0.0',
          'jsonpath-rw>=1.4.0,<2.0.0',
          'jsonpath-rw-ext>=1.2,<2.0',
          'jsonpath-extractor>=0.5.0,<0.8',
          'black>=20.8b1,<21.0',
          'flake8>=3.8.4,<4.0.0',
          'flake8-bugbear>=20.11.1,<21.0.0',
          'isort>=5.6.4,<6.0.0',
          'mypy>=0.812,<0.813',
          'pytest>=5.2.0,<6.0.0',
          'doc8>=0.8.0,<0.9.0',
          'pygments>=2.4,<3.0'],
 'lxml': ['lxml>=4.3.0,<5.0.0'],
 'test': ['pytest>=5.2.0,<6.0.0', 'pytest-cov>=2.7.1,<3.0.0']}

setup_kwargs = {
    'name': 'data-extractor',
    'version': '0.9.0',
    'description': 'Combine XPath, CSS Selectors and JSONPath for Web data extracting.',
    'long_description': '==============\nData Extractor\n==============\n\n|license| |Pypi Status| |Python version| |Package version| |PyPI - Downloads|\n|GitHub last commit| |Code style: black| |Build Status| |codecov|\n|Documentation Status|\n\nCombine **XPath**, **CSS Selectors** and **JSONPath** for Web data extracting.\n\nQuickstarts\n<<<<<<<<<<<\n\nInstallation\n~~~~~~~~~~~~\n\nInstall the stable version from PYPI.\n\n.. code-block:: shell\n\n    pip install "data-extractor[jsonpath-extractor]"  # for extracting JSON data\n    pip install "data-extractor[lxml]"  # for extracting HTML data\n\nOr install the latest version from Github.\n\n.. code-block:: shell\n\n    pip install "data-extractor[jsonpath-extractor] @ git+https://github.com/linw1995/data_extractor.git@master"\n\nExtract JSON data\n~~~~~~~~~~~~~~~~~\n\nCurrently supports to extract JSON data with below optional dependencies\n\n- jsonpath-extractor_\n- jsonpath-rw_\n- jsonpath-rw-ext_\n\n.. _jsonpath-extractor: https://github.com/linw1995/jsonpath\n.. _jsonpath-rw: https://github.com/kennknowles/python-jsonpath-rw\n.. _jsonpath-rw-ext: https://python-jsonpath-rw-ext.readthedocs.org/en/latest/\n\ninstall one dependency of them to extract JSON data.\n\nExtract HTML(XML) data\n~~~~~~~~~~~~~~~~~~~~~~\n\nCurrently supports to extract HTML(XML) data with below optional dependencies\n\n- lxml_ for using XPath_\n- cssselect_ for using CSS-Selectors_\n\n.. _lxml: https://lxml.de/\n.. _XPath: https://www.w3.org/TR/xpath-10/\n.. _cssselect: https://cssselect.readthedocs.io/en/latest/\n.. _CSS-Selectors: https://www.w3.org/TR/selectors-3/\n\nUsage\n~~~~~\n\n.. code-block:: python3\n\n    from data_extractor import Field, Item, JSONExtractor\n\n\n    class Count(Item):\n        followings = Field(JSONExtractor("countFollowings"))\n        fans = Field(JSONExtractor("countFans"))\n\n\n    class User(Item):\n        name_ = Field(JSONExtractor("name"), name="name")\n        age = Field(JSONExtractor("age"), default=17)\n        count = Count()\n\n\n    assert User(JSONExtractor("data.users[*]"), is_many=True).extract(\n        {\n            "data": {\n                "users": [\n                    {\n                        "name": "john",\n                        "age": 19,\n                        "countFollowings": 14,\n                        "countFans": 212,\n                    },\n                    {\n                        "name": "jack",\n                        "description": "",\n                        "countFollowings": 54,\n                        "countFans": 312,\n                    },\n                ]\n            }\n        }\n    ) == [\n        {"name": "john", "age": 19, "count": {"followings": 14, "fans": 212}},\n        {"name": "jack", "age": 17, "count": {"followings": 54, "fans": 312}},\n    ]\n\nChangelog\n<<<<<<<<<\n\nv0.9.0\n~~~~~~\n\n**Fix**\n\n- type annotations #63 #64\n\n**Refactor**\n\n- .utils.Property with "Customized names" support #64\n- rename .abc to .core and mark elder duplciated #65\n\n\n.. |license| image:: https://img.shields.io/github/license/linw1995/data_extractor.svg\n    :target: https://github.com/linw1995/data_extractor/blob/master/LICENSE\n\n.. |Pypi Status| image:: https://img.shields.io/pypi/status/data_extractor.svg\n    :target: https://pypi.org/project/data_extractor\n\n.. |Python version| image:: https://img.shields.io/pypi/pyversions/data_extractor.svg\n    :target: https://pypi.org/project/data_extractor\n\n.. |Package version| image:: https://img.shields.io/pypi/v/data_extractor.svg\n    :target: https://pypi.org/project/data_extractor\n\n.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/data-extractor.svg\n    :target: https://pypi.org/project/data_extractor\n\n.. |GitHub last commit| image:: https://img.shields.io/github/last-commit/linw1995/data_extractor.svg\n    :target: https://github.com/linw1995/data_extractor\n\n.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. |Build Status| image:: https://github.com/linw1995/data_extractor/workflows/Lint&Test/badge.svg\n    :target: https://github.com/linw1995/data_extractor/actions?query=workflow%3ALint%26Test\n\n.. |codecov| image:: https://codecov.io/gh/linw1995/data_extractor/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/linw1995/data_extractor\n\n.. |Documentation Status| image:: https://readthedocs.org/projects/data-extractor/badge/?version=latest\n    :target: https://data-extractor.readthedocs.io/en/latest/?badge=latest\n',
    'author': 'linw1995',
    'author_email': 'linw1995@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/linw1995/data_extractor',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
