# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_note_taker', 'simple_note_taker.core', 'simple_note_taker.subcommands']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'pydantic>=1.8.1,<2.0.0',
 'pytest-cov>=2.11.1,<3.0.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'rapidfuzz>=1.2.1,<2.0.0',
 'tinydb-serialization>=2.1.0,<3.0.0',
 'tinydb>=4.4.0,<5.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['snt = simple_note_taker.main:app']}

setup_kwargs = {
    'name': 'simple-note-taker',
    'version': '0.2.4',
    'description': 'A simple CLI Notetaker with magic commands and options for centralization and summaries for teams',
    'long_description': "A simple CLI note taker, written in Python.\n\nHome: https://github.com/GitToby/simple_note_taker\nPypi: https://pypi.org/project/simple-note-taker/\n\n# Features\n\n* Take notes via CLI and save to a flat json file.\n* Configure tasks and reminders in notes with magic commands such as `!task` and `!reminder`.\n* Search your notes with fuzzy matching or exact term matching.\n\n## Coming Soon\n* Optionally, share notes with other users via rest of the s3 protocol. Server app coming soon.\n* Summary commands will let you consolidate competed tasks, general notes and other items and share in a verity of methods.\n\n# Install\n\nVia `pip`\n\n```commandline\npip install simple_note_taker\n```\n\n# Usage.\n\n```commandline\nUsage: snt [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n\nCommands:\n  config     For interacting with configuration tooling\n  delete     Delete a note you've taken.\n  edit       Edit a note you've taken.\n  ls         Fetch the latest notes you've taken.\n  mark-done  Mark a task type note as done.\n  match      Search your notes you've saved previously which match a search...\n  search\n  size       Returns details on the size of you notes.\n  take       Take a note and save it.\n  tasks      Lists notes marked as Tasks.\n```\n\n# Dev Setup\n\nDev with [Poetry](https://python-poetry.org/). Run tests from root with `pytest`",
    'author': 'Toby Devlin',
    'author_email': 'toby@tobydevlin.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GitToby/simple_note_taker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
