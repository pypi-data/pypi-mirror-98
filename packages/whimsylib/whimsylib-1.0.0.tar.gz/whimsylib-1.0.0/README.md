[![PyPi version](https://img.shields.io/pypi/v/whimsylib.svg)](https://pypi.org/project/whimsylib/)

# whimsylib

A game engine for text-based games, inspired by [adventurelib](https://github.com/lordmauve/adventurelib).

This is currently the game engine behind [cronenbroguelike](https://github.com/Cronenbrogues/cronenbroguelike).

## Develop

Set up a virtualenv and install the dev requirements.

```
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements/requirements-dev.txt
```

## Release

Update the version number in `setup.py`, create the release files, and upload them to PyPI.

```
pip install -r requirements/requirements-release.txt
python setup.py sdist bdist_wheel
twine upload dist/*
```
