# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_append_array']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0']

extras_require = \
{':extra == "pandas"': ['pandas[pandas]>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'fast-append-array',
    'version': '0.2.0',
    'description': 'A dataframe which supports blazing fast append operations and column access by name.',
    'long_description': '# Fast Append Array\n\n\nA dataframe which allows access to columns by name and supports blazing fast append operations.\n\nOriginal repository: [https://github.com/mariushelf/fast\\_append\\_array](https://github.com/mariushelf/fast_append_array)\n\nAuthor: Marius Helf \n  ([helfsmarius@gmail.com](mailto:helfsmarius@gmail.com))\n\n\n# Changelog\n\n## 0.2.0\n* improve speed of `append_dict()` by factor 5\n* small improvements for element access and slicing\n* support for different dtypes\n* `from_pandas()` and `from_dicts()` functions\n\n## 0.1.0\n* first release\n\n# License\n\nMIT -- see [LICENSE](LICENSE)\n\n',
    'author': 'Marius Helf',
    'author_email': 'helfsmarius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mariushelf/fast_append_array',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
