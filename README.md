# Description

A project template. Search and replace all occurrences of `partest` and `template` to start using this template.



# Development
## Getting started

Assuming you have python >= 3.8 installed, you can run `source ./scripts/venv.py` to (re)create a clean venv.

Tests can be ran using `pytest tests`. 
This project is setup for usage through VSCode, which will interact for you with other configured tools, `black`, `flake8` and `mypy`.

## Publish

Publish to the test PyPI:

```bash
bash scripts/build.sh && \
python -m twine upload --repository testpypi dist/*
```
When prompted specify `__token__` for the username and the password from 1pass.

## Installation from test PyPI

```bash
python3 -m pip install --no-deps --index-url https://test.pypi.org/simple/ jeroenbos_partest_JEROEN_BOS
```

`--no-deps` is because dependencies are likely not on TestPyPI.