# MachineLearningMarchMadness

Predictive solution for March Madness bracket
Description:

- Goal: Predict the NCAA Mens Basketball tournament bracket using data scraped from the Web and a variety Machine Learning algorithms.

## If Notebook not loading in github
Use this [link](https://nbviewer.jupyter.org/github/SpicySyntax/MachineLearningMarchMadness/blob/master/MachineLearningMarchMadnessV1.ipynb)

## Prerequisites

- [Python 3.8](https://www.python.org/downloads/release/python-386/)
  - Or use Homebrew or Chocalatey
- [CMake](https://cmake.org/install/) (For XGBoost)
- [XGBoost](https://xgboost.readthedocs.io/en/latest/) use[brew](https://formulae.brew.sh/formula/xgboost) for Mac
- [Poetry](https://python-poetry.org/)


### Install Dependencies

```bash
pip install poetry
poetry install
# Activate shell
poetry shell
```

## Components

### Web Scraper:
  - Gathers [NCAA basketball data](https://www.sports-reference.com/cbb),
  - The scraper gathers regular season and post season game data and aggregate team statistics for the year range provided in scrape.py
      - Team Stats gathered (Team and Opponent)
        - `Per Game`: FG (Field Goal), 2P (Two Point), 3P (Three Point), ORB (Offensive Rebounds), DRB (Defensive Rebounds), AST (Assists),
            STL (Steals), BLK (Blocks), TOV (Turn Overs), PF (Personal Fouls), PTS (Points)
        - `Percentages`: FG (Field Goal), 2P (Two Point), 3P (Three Point), FT (Free-Throw), W/L (Win/Loss)
        - `Yearly`: SRS (Simple Rating System), SOS (Strength of Schedule)
        - Gather team stats above for each team. Each of these will be used as the data points to decide wins for each round. The training will occur based off of game outcomes.
    - (The scraped data is provided in the source `./Scraper`)
    - Note: Currently both solutions only train using post season game records

#### To Run Scraper
- Run:
```bash
poetry run python main.py
```


### Notebooks:
Jupyter Notebooks used to prepare the data and train the models

#### To start the notebooks

```bash
poetry run jupyter notebook
```

## Latest Results
[2021](./results/2021.md)

