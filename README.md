# Enforcing Code Quality

<!-- markdownlint-disable MD007 -->

<!-- TOC -->

- [Enforcing Code Quality](#enforcing-code-quality)
    - [YAML Linting](#yaml-linting)
    - [pre-commit hooks](#pre-commit-hooks)
    - [Pylint for python linting](#pylint-for-python-linting)

<!-- /TOC -->

## YAML Linting

- YAML linting with [custom configuration](https://yamllint.readthedocs.io/en/stable/configuration.html) for `.yamllint`

```bash
# check which files will be linted by default
yamllint --list-files .

# lint a specific file
yamllint my_file.yml

# OR
yamllint .
```

## [pre-commit hooks](https://github.com/pre-commit/pre-commit-hooks)

Pre-commit have been set up in this repo to check and fix for:

- missing lines at the end
- trailing whitespaces
- violations of sql standards
- errors in yaml syntax

Hence, when working with the repo, make sure you've got the pre-commit installed so that they run upon your every commit

```bash
# install the githook scripts
pre-commit install

# run against all existing files
pre-commit run --all-files
```

## [Pylint for python linting](https://pylint.readthedocs.io/en/latest/)

```bash
# lint a specific file
pylint my_file.py

# lint all Python files in the current directory
pylint .

# lint with a custom configuration file
pylint --rcfile=.pylintrc my_file.py
```
