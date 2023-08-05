# Time to submit while mobile working ヽ(´▽`)/
[![Python application](https://github.com/MikeGlotzkowski/timr/actions/workflows/python-app.yml/badge.svg)](https://github.com/MikeGlotzkowski/timr/actions/workflows/python-app.yml)
## Setup (currently)

### docker tryout one-liner 

```bash
 docker run -it --rm python:3.9-slim-buster python3 -m pip install timrr && python3 -m timrr calc
```

### locally

```bash
python3 -m pip install poetry
poetry install
poetry shell
poetry run python3 timrr.py
```

## Use the tool

```bash
❯ python3 -m timrr calc --start-time 8:15 --end-time 18:00 --break-time 1.0
| Description           | Result   |
|-----------------------+----------|
| Start time            | 08:15:00 |
| End time              | 18:00:00 |
| Duration at work      | 9:45:00  |
| Included break time   | 1.0      |
| Hours worked          | 8.75     |
| 1 day of mobile work  | 7.4      |
| Add extra mobile work | 1.35     |
```

```bash
❯ python3 -m timrr calc
| Description           | Result   |
|-----------------------+----------|
| Start time            | 09:00:00 |
| End time              | 17:30:00 |
| Duration at work      | 8:30:00  |
| Included break time   | 1.0      |
| Hours worked          | 7.5      |
| 1 day of mobile work  | 7.4      |
| Add extra mobile work | 0.1      |
```

```bash
❯ python3 -m timrr calc --help
Usage: timrr.py calc [OPTIONS]

Options:
  -s, --start-time TEXT
  -e, --end-time TEXT
  -b, --break-time TEXT
  -ch, --contract-hours-per-day TEXT
  --local-config / --no-local-config
  --help                          Show this message and exit.
```

## configure defaults

```bash
❯ python3 -m timrr configure
Provide a default start time of work: 8:00
Provide a default end time of work: 17:30
Provide a default break time: 1,25
Provide a default for work hours per day: 7.4
Configuration completed! (config file location: /home/tempusr/.timrr)
```

```bash
Usage: timrr.py configure [OPTIONS]

Options:
  --start-time TEXT              [required]
  --end-time TEXT                [required]
  --break-time TEXT              [required]
  --contract-hours-per-day TEXT  [required]
  --help                         Show this message and exit.
```
