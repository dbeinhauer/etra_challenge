# etra_challenge

Data Analysis of the ETRA Dataset.

## Setup

Firstly, you need to have [poetry](https://python-poetry.org/docs/) installed.
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Then setup the environment by running
```sh
poetry install
```

Finally, enter the environment
```sh
poetry shell
```

You can run ```jupyter lab``` from within the environment with all the required dependencies present.

## Generating report

To generate a html report run

```sh
jupyter nbconvert --to html etra_challenge_report.ipynb --execute --no-input --template pj
```