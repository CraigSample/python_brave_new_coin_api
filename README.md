# BraveNewCoin API Regression Suite

A short python example using the [BraveNewCoin API](https://rapidapi.com/BraveNewCoin/api/bravenewcoin) with pytest.

## Prerequisites

- Python 3.11
- pipenv
  - python3 -m pip install --user pipenv

## Manual Installation

Create a pipenv [virtual environment](https://pipenv.pypa.io/en/latest/)
to keep the dependencies isolated from your system's Python:
`pipenv install`

This step also installs the test suite's dependencies into the virtual env at
the same time by reading the included Pipfile.

## Configuration

To successfully run the suite, an [API key](https://rapidapi.com/BraveNewCoin/api/bravenewcoin/pricing) is required.
Populate the BNC_KEY value in support/constants.py with the key.

## Running Regression Suite

Issue the following to execute the entire test suite:
`pipenv run pytest`

### Custsom Markers

Marks are available to execute specific tests or subsets. See the [documentation](https://docs.pytest.org/en/7.1.x/example/markers.html) for details.

#### Available Marks

- asset: asset endpoint tests
- market: market endpoint tests
- negative: negative logic tests
- regression: regression tests
- token: token endpoint tests

#### Example

Run the market endpoint tests but exclude the negative logic tests:
`pipenv run pytest -m "market and not negative"`

## Reports

A basic output report is availble in the `report` directory. The file would normally be excluded from the repo, but was retained for an example.