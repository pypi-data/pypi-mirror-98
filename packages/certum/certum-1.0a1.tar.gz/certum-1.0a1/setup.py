# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['certum',
 'certum.rule.generic',
 'certum.rule.shared',
 'certum.strategy',
 'certum.strategy.filtering',
 'certum.strategy.printing',
 'certum.strategy.sorting']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'certum',
    'version': '1.0a1',
    'description': 'A dictionary validation library based on partial, composable and expressive rules.',
    'long_description': '# Certum\n\nA dictionary validation library based on partial, composable and expressive rules.\n\n## Why use it\n\nIn case you need to assert some propeties from a particular dictionary in a DSL manner without comparing the entire structure or asserting fields.\n\nCertum comes with the following features:\n- Easy to use\n- English friendly declaration\n- Error accumulation\n- Customizable\n- Anti KeyError\n\n## Using Certum\n\nYou can\'t use certum package for the moment, coming soon.\n\n## How it works\n\n### Basic usage\n\nImagine you have a very long json and you want to verify that it contains the following informations:\n- He should contains a key named \'name\' containing a string.\n- He should contains a key named \'entities\' being a list containing unique elements.\n- He should contains a key named \'nested\' containing a key \'value\' equals to 4.\n\n```python\nfrom certum import ensure, that\n\nmy_obj = {\n    "name": "hello",\n    "entities": [1, 3, 5],\n    "nested": {\n        "value": 4\n    }\n}\n\nvalidator = ensure(my_obj).respects(\n    that("name").is_instance_of(str),\n    that("entities").has_unique_elements(),\n    that("nested", "value").equals(4)\n)\n\nvalidator.check()\n```\n\n### Error handling\n\nIf there is errors, certum will accumulate and return errors elegantly:\n\n```python\nfrom certum import ensure, that\n\nmy_obj = {\n    "name": 2,\n    "entities": [1, 3, 3],\n    "nested": {\n        "value": 2\n    }\n}\n\nvalidator = (\n    ensure(my_obj)\n    .respects(\n        that("name").is_instance_of(str),\n        that("name").equals("Hello"),\n        that("entities").foreach(this.equals(1)),\n        that("nested", "value").equals(4),\n    )\n)\n\nvalidator.check()\n\n# certum.exception.CertumException: \n\n# [name] => The value is instance of int, expected str.\n# [name] => The value is 2, expected Hello.\n# [entities -> 2] => The value is 3, expected 1.\n# [entities -> 1] => The value is 3, expected 1.\n# [nested -> value] => The value is 2, expected 4.\n```\n\n### Strategies\n\nErros can be sorted, filtered and printed using different strategies.\n\nAs an example, you may want to try the GroupedPrinting strategy with the AlphabeticalSorting strategy, this will give you a list of errors like this:\n\n```python\nfrom certum import ensure, that, this\nfrom certum.strategy.printing.grouped import GroupedPrinting\nfrom certum.strategy.sorting.alphabetical import AlphabeticalSorting\n\n\nmy_obj = {\n    "name": 2,\n    "entities": [1, 3, 3],\n    "nested": {\n        "value": 2\n    }\n}\n\nvalidator = (\n    ensure(my_obj)\n    .respects(\n        that("name").is_instance_of(str),\n        that("name").equals("Hello"),\n        that("entities").foreach(this.equals(1)),\n        that("nested", "value").equals(4),\n    )\n    .using(GroupedPrinting(), AlphabeticalSorting())\n)\n\nvalidator.check()\n\n# certum.exception.CertumException: \n\n# entities -> 1   => The value is 3, expected 1.\n# entities -> 2   => The value is 3, expected 1.\n# name            => The value is 2, expected Hello.\n#                    The value is instance of int, expected str.\n# nested -> value => The value is 2, expected 4.\n```\n',
    'author': 'dylandoamaral',
    'author_email': 'do.amaral.dylan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dylandoamaral/certum',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
