# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colorboy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['test = test:test']}

setup_kwargs = {
    'name': 'colorboy',
    'version': '1.0.3',
    'description': 'Easily add color to your strings',
    'long_description': "# colorboy\n\nEasily add color to your strings\n\n## Installation\n\n```\npip install colorboy\n```\n\n## Usage\n\n```python\nimport colorboy as cb\nprint(cb.cyan('Globgogabgalab'))\n\n# import specific colors, bg_colors and styles\nfrom colorboy import white_bg, black\nprint(white_bg(black('Pog')))\n\n# import everything\nfrom colorboy import *\nprint(green('Mayonnaise'))\n\nfrom colorboy.colors import * # import all colors\nprint(red('EDEN'))\nfrom colorboy.bg_colors import * # import all bg_colors\nprint(black_bg('Stephen'))\nfrom colorboy.styles import * # import all styles\nprint(bright('Crywolf'))\n```\n\n## Colors\nThese are all the color functions available through colorboy:\n\n```python\n# colors - available by importing colorboy or colorboy.colors\nblack\nred\ngreen\nyellow\nblue\nmagenta\ncyan\nwhite\n\n# bg_colors - available by importing colorboy or colorboy.bg_colors\nblack_bg\nred_bg\ngreen_bg\nyellow_bg\nblue_bg\nmagenta_bg\ncyan_bg\nwhite_bg\n\n# styles - available by importing colorboy or colorboy.styles\ndim\nbright\n```\n\n## Dev Instructions\n\n### Get started\n\n1. Install Python (Python 3.7 works, probably other versions too)\n2. Install [Poetry](https://poetry.eustace.io). Poetry is used to manage dependencies, the virtual environment and publishing to PyPI, so it's worth learning\n3. Run `poetry install` to install Python package dependencies\n\nI recommend running `poetry config virtualenvs.in-project true`, which makes Poetry store your Python virtual environment inside the project folder. Additionally, it lets VSCode's Python extension detect the virtual environment if you set the `python.pythonPath` setting to `${workspaceFolder}/.venv/bin/python` in your settings.\n\n### Running\n\nTo test if things work, you can run the following command to open the Python REPL. Then you can write Python, such as the usage examples:\n\n```\npoetry run python\n```\n\n### Releasing a new version\n\n1. Consider updating the lockfile by running `poetry update`, then check if thing still work\n2. Bump the version number:\n    ```\n    poetry version <version>\n    ```\n3. Update `CHANGELOG.md`\n4. Build:\n    ```\n    poetry build\n    ```\n5. Commit and create git tag\n6. Create GitHub release with release notes and attach the build files\n7. Publish to PyPi:\n    ```\n    poetry publish\n    ```\n",
    'author': 'kasper.space',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/probablykasper/colorboy-py',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
