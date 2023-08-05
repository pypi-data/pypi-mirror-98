# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prevent_submodule_regression']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['prevent-submodule-regression = '
                     'prevent_submodule_regression.cli:main']}

setup_kwargs = {
    'name': 'prevent-submodule-regression',
    'version': '0.1.3',
    'description': 'Pre-commit hook to prevent accidental submodule regressions',
    'long_description': '# prevent-submodule-regression\n\nPre-commit hook to prevent accidental submodule regressions\n\n## Description\n\nDo you find yourself (or your collaborators) constantly rolling back submodule\nSHAs because someone forgot to `git submodule update` before running `git add\n.` or `git commit -a …`?\n\nThis pre-commit plugin will prevent those nasty surprises from making their\nway into your repositories.\n\n## Installation\n\n### As a git hook\n\nThe simplest way to use this package is as a plugin to [pre-commit](https://pre-commit.com/).\n\nA sample configuration:\n\n```yaml\nrepos:\n  # […]\n  - repo: https://github.com/erikogan/prevent-submodule-regression\n    rev: v0.1.3\n    hooks:\n      - id: prevent-submodule-regression\n        # By default hooks only operate on plain files, which do not include\n        # submodules. This setting has been added to the hook configuration,\n        # and should only be necessary if you are running a version older than\n        # 0.1.3. Keeping it here for posterity, it can safely be skipped.\n        types: [directory]\n```\n\nExample failure output:\n\n![submodule example with colorized output](https://user-images.githubusercontent.com/60583/89809067-ec04d500-daef-11ea-9d43-7e990ea21234.png)\n\n\n### As a standalone script\n\n```\npip install prevent-submodule-regression [path…]\n```\n\nIf you run the script with no arguments, it will automatically find all the\nconfigured submodules. You can also pass it a list of files to check.\n\nIt will currently ignore any path that is not staged to be commit. A future\nversion of the script will have an argument to override that behavior.\n\n## TODO\n\nIn no particular order:\n\n* Actual tests\n* Ways to override the error and allow you to commit a regression.\n  * Command-line\n  * Environment variables\n* Ways to override (or disable) colorization codes\n  * Command-line\n  * Environment variables\n* Usage information via `--help`\n* Actual command-line flag parsing\n',
    'author': 'Erik Ogan',
    'author_email': 'erik@ogan.net',
    'maintainer': 'Erik Ogan',
    'maintainer_email': 'erik@ogan.net',
    'url': 'https://github.com/erikogan/prevent-submodule-regression',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
