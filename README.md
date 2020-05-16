# Task Puzzle 15 Terminal Python Application
https://en.wikipedia.org/wiki/15_puzzle

This is a python implementation of Puzzle 15 using terminal.

## How to Run
### Prerequisites
Make sure your system has installed [Python3](https://www.python.org/downloads/), [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) and [pip](https://pip.pypa.io/en/stable/installing/)
```
python3 --version
pip3 --version
```

### Setup Virtualenv
```
virtualenv venv
source venv/bin/activate
```

### Run Puzzle 15 App
Install all dependencies
```
make init
```

(Optional) Change arguments in `run.sh` file. Default arguments:
```
ROWS_NUMBER=4
COLS_NUMBER=4
DEBUG=false
```

Run tests:
```
make test
```

Run tests and show coverage report:
```
make coverage
```

Run app:
```
make run
```
