# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pretty_poly']

package_data = \
{'': ['*']}

install_requires = \
['pypng>=0.0.20,<0.0.21']

entry_points = \
{'console_scripts': ['doctest = run_tests:run_doctest',
                     'examples = examples.make:write_examples',
                     'test = run_tests:test']}

setup_kwargs = {
    'name': 'pretty-poly',
    'version': '0.3.2a0',
    'description': 'Display polyominos and polyomino tilings in various pretty formats.',
    'long_description': '# pretty_poly - a package for displaying polyomino tilings\n\nThis is a Python package for displaying polyomino tilings, expressed as lists of lists of (x, y) tuples, in various ways.\n\n\n```\n>>> from pretty_poly import make_ascii\n>>> print(make_ascii([[(0, 0), (0, 1), (0, 2), (1, 1)], [(0, 3), (1, 3), (2, 3), (1, 2)], [(1, 0), (2, 0), (3, 0), (2, 1)], [(3, 1), (3, 2), (2, 2)]]))\n+-+-+-+-+\n| |     |\n+ +-+ +-+\n|   | | |\n+ +-+-+ +\n| | |   |\n+-+ +-+-+\n|     |\n+-+-+-+\n\n```\n\n## How to cite this code:\n```\n@misc{pretty_poly,\n  author = {Jack Grahl},\n  title = {pretty_poly - a package for displaying polyomino tilings},\n  year = {2021},\n  howpublished = {\\url{https://github.com/jwg4/pretty_poly}},\n  commit = {...}\n}\n```\n',
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jwg4/pretty_poly',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
