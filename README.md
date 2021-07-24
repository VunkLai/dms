# Data Management System

For Joy

## Requirements

Data Management System requires the following:

- Python 3.8+
  - pipenv
- Django 3.0+

The following packages are required:

- django-environ
- pymssql

for test you need:

- pylint
- pylint-django
- bandit

## Quick Start

```bash
git clone https://github.com/VunkLai/dms.git
cd dms
pip3 install pipenv
pipenv install
pipenv shell
python dms/manage.py migrate
python dms/manage.py runserver
```

## Test

```bash
pipenv install -d
pipenv shell

sh bin/test.py # generic tests
python manage.py test dms # unittest
```

### Generic

1. Security check
   - pipenv check
   - ~~safety~~
2. Linting
   - pylint + pylint-django
3. Static Analysis
   - bandit

### Unit-test / Functional-test

```bash
cd dms
python manage.py check
python manage.py test dms
```

### SI test

skip

## TODO

1. [x] PE PSMC excel
2. [x] HR Gateway
3. [ ] HR Gateway summary
4. [ ] HR Health declaration
5. [ ] FIN Cost center
