# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['timrr']
install_requires = \
['click>=7.1.2,<8.0.0', 'tabulate>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'timrr',
    'version': '1.0.1',
    'description': 'Time to submit while mobile working',
    'long_description': '# Time to submit while mobile working ヽ(´▽`)/\n[![Python application](https://github.com/MikeGlotzkowski/timr/actions/workflows/python-app.yml/badge.svg)](https://github.com/MikeGlotzkowski/timr/actions/workflows/python-app.yml)\n## Setup (currently)\n\n### docker tryout one-liner \n\n```bash\n docker run -it --rm python:3.9-slim-buster python3 -m pip install timrr && python3 -m timrr calc\n```\n\n### locally\n\n```bash\npython3 -m pip install poetry\npoetry install\npoetry shell\npoetry run python3 timrr.py\n```\n\n## Use the tool\n\n```bash\n❯ python3 -m timrr calc --start-time 8:15 --end-time 18:00 --break-time 1.0\n| Description           | Result   |\n|-----------------------+----------|\n| Start time            | 08:15:00 |\n| End time              | 18:00:00 |\n| Duration at work      | 9:45:00  |\n| Included break time   | 1.0      |\n| Hours worked          | 8.75     |\n| 1 day of mobile work  | 7.4      |\n| Add extra mobile work | 1.35     |\n```\n\n```bash\n❯ python3 -m timrr calc\n| Description           | Result   |\n|-----------------------+----------|\n| Start time            | 09:00:00 |\n| End time              | 17:30:00 |\n| Duration at work      | 8:30:00  |\n| Included break time   | 1.0      |\n| Hours worked          | 7.5      |\n| 1 day of mobile work  | 7.4      |\n| Add extra mobile work | 0.1      |\n```\n\n```bash\n❯ python3 -m timrr calc --help\nUsage: timrr.py calc [OPTIONS]\n\nOptions:\n  -s, --start-time TEXT\n  -e, --end-time TEXT\n  -b, --break-time TEXT\n  -ch, --contract-hours-per-day TEXT\n  --local-config / --no-local-config\n  --help                          Show this message and exit.\n```\n\n## configure defaults\n\n```bash\n❯ python3 -m timrr configure\nProvide a default start time of work: 8:00\nProvide a default end time of work: 17:30\nProvide a default break time: 1,25\nProvide a default for work hours per day: 7.4\nConfiguration completed! (config file location: /home/tempusr/.timrr)\n```\n\n```bash\nUsage: timrr.py configure [OPTIONS]\n\nOptions:\n  --start-time TEXT              [required]\n  --end-time TEXT                [required]\n  --break-time TEXT              [required]\n  --contract-hours-per-day TEXT  [required]\n  --help                         Show this message and exit.\n```\n',
    'author': 'MikeGlotzkowski',
    'author_email': 'sebastian.lischewski@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
