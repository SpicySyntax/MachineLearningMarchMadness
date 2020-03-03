# MachineLearningMarchMadness

Predictive solution for March Madness bracket
Description:

- Predict the NCAA tournament bracket using data scraped from the Web and a variety Machine Learning algorithms.

## If Notebook not loading in github
Use this [link](https://nbviewer.jupyter.org/github/SpicySyntax/MachineLearningMarchMadness/blob/master/Notebooks/MachineLearningMarchMadnessV1.ipynb)

## Prerequisites

- [Python 3.7](https://www.python.org/downloads/release/python-376/)
- [CMake](https://cmake.org/install/) (For XGBoost)
- [Chrome Driver](https://chromedriver.chromium.org/downloads) (noting the executable path)

### Install Dependencies

```bash
pip install pipenv
pipenv shell
pipenv install
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
- set the `chrome_exe` path to your chrome executable in `scraper.py`
- Run:
```bash
python scraper.py
```


### Notebooks:
Jupyter Notebooks used to prepare the data and train the models

#### To start the notebooks

```bash
pipenv run jupyter notebook
```

## Results (Version 1 with new data and Logistic Regression in March 2019 82.8 percentile)

### Did great with the Auburn Prediction though! Got 2nd in work bracket and 1st in personal bracket

- --- East  round  1 ---
  - Duke 1  vs.  North Carolina Central 16 (team 1 won= 1 )
  - VCU 8  vs.  UCF 9 (team 1 won= 1 )
  - Mississippi State 5  vs.  Liberty 12 (team 1 won= 1 )
  - Virginia Tech 4  vs.  Saint Louis 13 (team 1 won= 1 )
  - Maryland 6  vs.  Temple 11 (team 1 won= 1 )
  - LSU 3  vs.  Yale 14 (team 1 won= 1 )
  - Louisville 7  vs.  Minnesota 10 (team 1 won= 1 )
  - Michigan State 2  vs.  Bradley 15 (team 1 won= 1 )
- --- East  round  2 ---
  - Duke 1  vs.  VCU 8 (team 1 won= 1 )
  - Mississippi State 5  vs.  Virginia Tech 4 (team 1 won= 0 )
  - Maryland 6  vs.  LSU 3 (team 1 won= 0 )
  - Louisville 7  vs.  Michigan State 2 (team 1 won= 0 )
- --- East  round  3 ---
  - Duke 1  vs.  Virginia Tech 4 (team 1 won= 1 )
  - LSU 3  vs.  Michigan State 2 (team 1 won= 0 )
- --- East  round  4 ---
  - Duke 1  vs.  Michigan State 2 (team 1 won= 1 )
  - Winner of  East : ('Duke', 1)
- --- West  round  1 ---
  - Gonzaga 1  vs.  Prairie View 16 (team 1 won= 1 )
  - Syracuse 8  vs.  Baylor 9 (team 1 won= 1 )
  - Marquette 5  vs.  Murray State 12 (team 1 won= 1 )
  - Florida State 4  vs.  Vermont 13 (team 1 won= 1 )
  - Buffalo 6  vs.  Arizona State 11 (team 1 won= 1 )
  - Texas Tech 3  vs.  Northern Kentucky 14 (team 1 won= 1 )
  - Nevada 7  vs.  Florida 10 (team 1 won= 0 )
  - Michigan 2  vs.  Montana 15 (team 1 won= 1 )
- --- West  round  2 ---
  - Gonzaga 1  vs.  Syracuse 8 (team 1 won= 1 )
  - Marquette 5  vs.  Florida State 4 (team 1 won= 0 )
  - Buffalo 6  vs.  Texas Tech 3 (team 1 won= 0 )
  - Florida 10  vs.  Michigan 2 (team 1 won= 0 )
- --- West  round  3 ---
  - Gonzaga 1  vs.  Florida State 4 (team 1 won= 1 )
  - Texas Tech 3  vs.  Michigan 2 (team 1 won= 1 )
- --- West  round  4 ---
  - Gonzaga 1  vs.  Texas Tech 3 (team 1 won= 1 )
  - Winner of  West : ('Gonzaga', 1)
- --- South  round  1 ---
  - Virginia 1  vs.  Gardner-Webb 16 (team 1 won= 1 )
  - Ole Miss 8  vs.  Oklahoma 9 (team 1 won= 0 )
  - Wisconsin 5  vs.  Oregon 12 (team 1 won= 1 )
  - Kansas State 4  vs.  UC-Irvine 13 (team 1 won= 1 )
  - Villanova 6  vs.  Saint Mary's 11 (team 1 won= 0 )
  - Purdue 3  vs.  Old Dominion 14 (team 1 won= 1 )
  - Cincinnati 7  vs.  Iowa 10 (team 1 won= 1 )
  - Tennessee 2  vs.  Colgate 15 (team 1 won= 1 )
- --- South  round  2 ---
  - Virginia 1  vs.  Oklahoma 9 (team 1 won= 1 )
  - Wisconsin 5  vs.  Kansas State 4 (team 1 won= 1 )
  - Saint Mary's 11  vs.  Purdue 3 (team 1 won= 0 )
  - Cincinnati 7  vs.  Tennessee 2 (team 1 won= 0 )
- --- South  round  3 ---
  - Virginia 1  vs.  Wisconsin 5 (team 1 won= 1 )
  - Purdue 3  vs.  Tennessee 2 (team 1 won= 1 )
- --- South  round  4 ---
  - Virginia 1  vs.  Purdue 3 (team 1 won= 1 )
  - Winner of  South : ('Virginia', 1)
- --- MidWest  round  1 ---
  - UNC 1  vs.  Iona 16 (team 1 won= 1 )
  - Utah State 8  vs.  Washington 9 (team 1 won= 0 )
  - Auburn 5  vs.  New Mexico State 12 (team 1 won= 1 )
  - Kansas 4  vs.  Northeastern 13 (team 1 won= 1 )
  - Iowa State 6  vs.  Ohio State 11 (team 1 won= 1 )
  - Houston 3  vs.  Georgia State 14 (team 1 won= 1 )
  - Wofford 7  vs.  Seton Hall 10 (team 1 won= 1 )
  - Kentucky 2  vs.  Abilene Christian 15 (team 1 won= 1 )
- --- MidWest  round  2 ---
  - UNC 1  vs.  Washington 9 (team 1 won= 0 )
  - Auburn 5  vs.  Kansas 4 (team 1 won= 1 )
  - Iowa State 6  vs.  Houston 3 (team 1 won= 1 )
  - Wofford 7  vs.  Kentucky 2 (team 1 won= 1 )
- --- MidWest  round  3 ---
  - Washington 9  vs.  Auburn 5 (team 1 won= 0 )
  - Iowa State 6  vs.  Wofford 7 (team 1 won= 1 )
- --- MidWest  round  4 ---
  - Auburn 5  vs.  Iowa State 6 (team 1 won= 1 )

- --- FinalFour  round  1 ---
  - Duke 1  vs.  Gonzaga 1 (team 1 won= 1 )
  - Virginia 1  vs.  Auburn 5 (team 1 won= 0 )
- --- FinalFour  round  2 ---
  - Duke 1  vs.  Auburn 5 (team 1 won= 0 )
  - Winner of  FinalFour : ('Auburn', 5)
  - Winner of  MidWest : ('Auburn', 5)

## Results (Version 1 calculated using Logistic Regression in March 2018 ~90th percentile (If I remember correctly))

### Got 2nd in both work brackets and personal brackets

  (Using regular season team statistics, matchup data from 2011-2017 post season games and Logistic Regression):

- --- South  round  1 ---
  - Virginia 1  vs.  Maryland-Baltimore County 16 (team 1 won= True )
  - Creighton 8  vs.  Kansas State 9 (team 1 won= True )
  - Kentucky 5  vs.  Davidson 12 (team 1 won= True )
  - Arizona 4  vs.  Buffalo 13 (team 1 won= True )
  - Miami (FL) 6  vs.  Loyola (IL) 11 (team 1 won= True )
  - Tennessee 3  vs.  Wright State 14 (team 1 won= True )
  - Nevada 7  vs.  Texas 10 (team 1 won= False )
  - Cincinnati 2  vs.  Georgia State 15 (team 1 won= True )
  
- --- South  round  2 ---
  - Virginia 1  vs.  Creighton 8 (team 1 won= True )
  - Kentucky 5  vs.  Arizona 4 (team 1 won= True )
  - Miami (FL) 6  vs.  Tennessee 3 (team 1 won= True )
  - Texas 10  vs.  Cincinnati 2 (team 1 won= False )
  
- --- South  round  3 ---
  - Virginia 1  vs.  Kentucky 5 (team 1 won= True )
  - Miami (FL) 6  vs.  Cincinnati 2 (team 1 won= False )
  
- --- South  round  4 ---
  - Virginia 1  vs.  Cincinnati 2 (team 1 won= True )
  - Winner of  South : ('Virginia', 1)
  
- --- West  round  1 ---
  - Xavier 1  vs.  North Carolina Central 16 (team 1 won= True )
  - Missouri 8  vs.  Florida State 9 (team 1 won= False )
  - Ohio State 5  vs.  South Dakota State 12 (team 1 won= True )
  - Gonzaga 4  vs.  North Carolina-Greensboro 13 (team 1 won= True )
  - Houston 6  vs.  San Diego State 11 (team 1 won= True )
  - Michigan 3  vs.  Montana 14 (team 1 won= True )
  - Texas A&M 7  vs.  Providence 10 (team 1 won= True )
  - North Carolina 2  vs.  Lipscomb 15 (team 1 won= True )
  
- --- West  round  2 ---
  - Xavier 1  vs.  Florida State 9 (team 1 won= False )
  - Ohio State 5  vs.  Gonzaga 4 (team 1 won= True )
  - Houston 6  vs.  Michigan 3 (team 1 won= True )
  - Texas A&M 7  vs.  North Carolina 2 (team 1 won= False )
  
- --- West  round  3 ---
  - Florida State 9  vs.  Ohio State 5 (team 1 won= True )
  - Houston 6  vs.  North Carolina 2 (team 1 won= False )
  
- --- West  round  4 ---
  - Florida State 9  vs.  North Carolina 2 (team 1 won= False )
  - Winner of  West : ('North Carolina', 2)
  
- --- East  round  1 ---
  - Villanova 1  vs.  Long Island University 16 (team 1 won= True )
  - Virginia Tech 8  vs.  Alabama 9 (team 1 won= True )
  - West Virginia 5  vs.  Murray State 12 (team 1 won= True )
  - Wichita State 4  vs.  Marshall 13 (team 1 won= True )
  - Florida 6  vs.  St. Bonaventure 11 (team 1 won= True )
  - Texas Tech 3  vs.  Stephen F. Austin 14 (team 1 won= True )
  - Arkansas 7  vs.  Butler 10 (team 1 won= True )
  - Purdue 2  vs.  Cal State Fullerton 15 (team 1 won= True )
  
- --- East  round  2 ---
  - Villanova 1  vs.  Virginia Tech 8 (team 1 won= True )
  - West Virginia 5  vs.  Wichita State 4 (team 1 won= True )
  - Florida 6  vs.  Texas Tech 3 (team 1 won= False )
  - Arkansas 7  vs.  Purdue 2 (team 1 won= False )
  
- --- East  round  3 ---
  - Villanova 1  vs.  West Virginia 5 (team 1 won= True )
  - Texas Tech 3  vs.  Purdue 2 (team 1 won= False )
  
- --- East  round  4 ---
  - Villanova 1  vs.  Purdue 2 (team 1 won= True )
  - Winner of  East : ('Villanova', 1)
  
- --- MidWest  round  1 ---
  - Kansas 1  vs.  Pennsylvania 16 (team 1 won= True )
  - Seton Hall 8  vs.  North Carolina State 9 (team 1 won= True )
  - Clemson 5  vs.  New Mexico State 12 (team 1 won= True )
  - Auburn 4  vs.  College of Charleston 13 (team 1 won= True )
  - Texas Christian 6  vs.  Arizona State 11 (team 1 won= False )
  - Michigan State 3  vs.  Bucknell 14 (team 1 won= True )
  - Rhode Island 7  vs.  Oklahoma 10 (team 1 won= False )
  - Duke 2  vs.  Iona 15 (team 1 won= True )
  
- --- MidWest  round  2 ---
  - Kansas 1  vs.  Seton Hall 8 (team 1 won= True )
  - Clemson 5  vs.  Auburn 4 (team 1 won= True )
  - Arizona State 11  vs.  Michigan State 3 (team 1 won= False )
  - Oklahoma 10  vs.  Duke 2 (team 1 won= False )
  
- --- MidWest  round  3 ---
  - Kansas 1  vs.  Clemson 5 (team 1 won= True )
  - Michigan State 3  vs.  Duke 2 (team 1 won= False )
  
- --- MidWest  round  4 ---
  - Kansas 1  vs.  Duke 2 (team 1 won= False )
  - Winner of  MidWest : ('Duke', 2)
  
- --- FinalFour  round  1 ---
  - Virginia 1  vs.  North Carolina 2 (team 1 won= True )
  - Villanova 1  vs.  Duke 2 (team 1 won= True )
  
- --- FinalFour  round  2 ---
  - Virginia 1  vs.  Villanova 1 (team 1 won= True )
  - Winner of  FinalFour : ('Virginia', 1)

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
  - Look into LSTM implementation if time permits

- Improve method for prediction
  - Investigate performance of XG Boost to Logistic Regression (May be better for this type of tabular data)

