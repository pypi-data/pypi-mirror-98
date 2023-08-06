# {{cookiecutter.project}}

[![Pipeline][pipeline-badge]][pipeline-link]
[![Coverage][coverage-badge]][coverage-link]
[![Documentation][documentation-badge]][documentation-link]
[![PyPI][pypi-badge]][pypi-link]

[pipeline-badge]: {{cookiecutter.repository_url}}/badges/master/pipeline.svg
[pipeline-link]: {{cookiecutter.repository_url}}/pipelines
[coverage-badge]: {{cookiecutter.repository_url}}/badges/master/coverage.svg
[coverage-link]: {{cookiecutter.repository_url}}/-/jobs
[documentation-badge]: https://readthedocs.org/projects/{{cookiecutter.project}}/badge/?version=stable
[documentation-link]: http://{{cookiecutter.project}}.readthedocs.org/stable/
[pypi-badge]: https://img.shields.io/pypi/v/{{cookiecutter.project}}.svg
[pypi-link]: https://pypi.python.org/pypi/{{cookiecutter.project}}

## Features

## Technical requirements

Below is the list of currently supported Python releases:

| # | Python |
|---|--------|
| 1 | 3.6    |
| 2 | 3.7    |
| 3 | 3.8    |
| 4 | 3.9    |

## Code and contribution

The code is open source and released under the [MIT License (MIT)][mit-license]. It is available on [Gitlab][gitlab] and follows the guidelines about [Semantic Versioning][semver] for transparency within the release cycle and backward compatibility whenever possible.

All contributions are welcome, whether bug reports, reviews, documentation or feature requests.

If you're a developer and have time and ideas for code contributions, fork the repo and prepare a merge request:

```bash
# Prepare your environment the first time
mkvirtualenv --python=python3.6 {{cookiecutter.project}}-py36
pip install -e .[development]

# Running the tests while development
pytest

# Individual Python release tests and code quality checks
tox -e py36
tox -e coverage
tox -e flake8

# Ensure code quality running the entire test suite,
# this requires all supported Python releases to be installed
tox
```

[mit-license]: https://en.wikipedia.org/wiki/MIT_License
[gitlab]: {{cookiecutter.repository_url}}
[semver]: http://semver.org/

## Installation

Install `{{cookiecutter.project}}` using pip:

```bash
pip install {{cookiecutter.project}}
```

## Usage
