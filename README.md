# MachineLearningMarchMadness
Predictive solution for March Madness bracket
Description: 
  - Predict the NCAA tournament bracket using data scraped from the Web and Machine Learning algorithms.

## Components
  - `Web Scraper`:
    - uses Python 3.7.0,
    - use 'pip3' to install `csv` and `selenium` for the web scraper.
    - to gather the data from https://www.sports-reference.com/cbb run `python scraper.py`
      - The scraper gathers regular season and post season game data and aggregate team statistics for the year range provided in scrape.py
      - Team Stats gathered (Team and Opponent)
        -	`Per Game`: FG (Field Goal), 2P (Two Point), 3P (Three Point), ORB (Offensive Rebounds), DRB (Defensive Rebounds), AST (Assists),
            STL (Steals), BLK (Blocks), TOV (Turn Overs), PF (Personal Fouls), PTS (Points)
        -	`Percentages`: FG (Field Goal), 2P (Two Point), 3P (Three Point), FT (Free-Throw), W/L (Win/Loss)
        -	`Yearly`: SRS (Simple Rating System), SOS (Strength of Schedule)
        -Plan, gather team stats above for each team. Each of these will be used as the data points to decide wins for each round. The training will occur based off of game outcomes.
      - (The scraped data is provided in the source `./Scraper`)
      - Note: Currently both solutions only train using post season game records

  - `Notebook (Python 3)`:
    - Download Jupyter notebooks through conda or pip (see https://test-jupyter.readthedocs.io/en/rtd-theme/install.html).
    - OR You can jupyter-notebooks via docker containers (see : https://hub.docker.com/r/jupyter/datascience-notebook/ for details)
      - If you don't have docker installed, install it (I used docker for windows)
      - Get Docker image for data-science notebook `docker pull jupyter/datascience-notebook`
      - To run use: `docker run -p 8888:8888 jupyter/datascience-notebook`
      - Connect to the notebook service at 'http://localhost:8888'
      - Upload the '.ipynb' and the CSV data from the scraper directory into the workspace using Jupyter's notebook interface, or by mounting a volume with the correct files.
      - If you upload through the interface, Copy files out of container using `docker cp <containerId>:/file/path/within/container       /host/path/target`. If you mount a volume into the container then you are okay.
      -manipulate which model you want to use to generate bracker by changing the model used in "evaluate_winner" function to one of the previous models used in the notebook.
      - If your python kernels keep dying increase the Memory allowed for docker containers in Docker > Settings
  
  ## Results (Version 1 calculated using Logistic Regression in March 2018)
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
## V2 Goals:
  - Improve the data
    - Further clean the data, remove correlated variables (see https://developers.google.com/machine-learning/crash-course/representation/cleaning-data)
    - Add some artificial features?
    - Take in game locations and team locations to calculate travel distance as a feature for both teams (Consider adding home, away, and neutral to model)
    - Remove outliers, or incorrect values (- when supposed to be +)
    - Use Pytorch to train a Neural network (done)
    - Normalize feature vectors (done)
    - Start with basic MLP with dropout and normalized inputsn (done)
    - Introduce Dropout (done)
    - Add validation splits and only save model when validation fails (done)
    - Augment the data set with regular season games + stats (create artificial rank using team statistics => train a model for this)
    - Look into LSTM implementation if time permits
  - Improve method for prediction
    - Use Evolutionary method to optimize hyper-parameters (learning rate batch size)
    - Predict both team scores instead of outcome?
    - Boost low seed stats if they beat a high seed, reduce high seed stats if they have close game with lower seed
  
