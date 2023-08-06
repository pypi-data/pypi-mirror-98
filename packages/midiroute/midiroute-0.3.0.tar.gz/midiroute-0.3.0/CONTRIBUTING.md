# Contributing to midiroute

Thanks for deciding to contribute to this project! Here are a few tips for
how to contribute, and how to get your contributions accepted.

## Contribution Workflow

1. Raise an issue requesting a new feature (or reporting a defective one).
1. Fork the repository.
1. Commit your changes to your fork.
1. Raise a PR against our master branch.

PRs must pass the required CI checks before they can be merged.

## Code Style

* We use black with default settings to format our code.
* Docstrings follow the [google style](http://google.github.io/styleguide/pyguide.html#381-docstrings).

## Tests

We use `pytest` to run our test suite. Our expectation is that contributions
always come with unit tests. A high level of test coverage is enforced by the
CI.

## Local Development Environment

To set up a local development environment, first clone the `midiroute`
repository.

```
git clone git@github.com/atticave/midiroute.git && cd midiroute
```

Run linting checks (we run `black` and `flake8` among others).

```
tox -e linting
```

Run the typing checks using mypy.

```
tox -e typing
```

Run the test suite.

```
tox -e py39
```

You can also set up a dev environment using `tox`.
```
tox -e dev
```

Activate the dev environment.

```
source .venv/bin/activate
```

You can now run `pytest` directly

```
pytest
```

The dev env contains all of the linting tools, and pytest, so your IDE can
easily pick them up if it is python aware. Most python-savvy IDEs will
auto-detect the `.venv` folder, and should work pretty well with this setup.

Have fun!
