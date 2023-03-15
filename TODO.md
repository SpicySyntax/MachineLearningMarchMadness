## V3 Goals

- Enter Kaggle Competition in 2020 (Invesigate new data): https://www.kaggle.com/c/mens-machine-learning-competition-2019
- Improve the data
  - Further clean the data, remove correlated variables (see https://developers.google.com/machine-learning/crash-course/representation/cleaning-data)
  - Add some artificial features:
    - Use last 5 game before tournament win/loss ratio as additional feature
    - Take in game locations and team locations to calculate travel distance as a feature for both teams (Consider adding home, away, and neutral to model)
    - One-hot encode the team seed
    - Add tournament appearances in last 2 years
  - Remove outliers, or incorrect values (- when supposed to be +)
  - Augment the data set with regular season games + stats (create artificial rank using team statistics => train a model for this)

- reduce manual work needed to be completed each year
 - auto populate tournament data after selection sunday
 - incremental data load (document)

- Improve method for prediction
  - Investigate performance of XG Boost to Logistic Regression (May be better for this type of tabular data)

- Tournament results visualization

- Refactoring
  - cleanup messy code
  - add tests
  - move model training into python from jupyter notebook?

- Rename?
  - march-ml

- master -> main

  
