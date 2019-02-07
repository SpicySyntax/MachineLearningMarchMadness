# MachineLearningMarchMadness
Predictive solution for March Madness bracket
Description: 
  - Try to predict the NCAA tournament bracket. Scrape data from the web and used ML to predict the outcomes of games

## Components
  - Web Scraper:
    - uses Python 2.7.14,
    - use 'pip' to install `csv` and `selenium` for the web scraper,
  - Notebook:
    - uses jupyter-notebooks via docker containers (see : https://hub.docker.com/r/jupyter/datascience-notebook/ for details) 
      - If you don't have docker installed, install it (I used docker for windows)
      - To run I used: `docker run -d -p 8888:8888 jupyter/datascience-notebook start-notebook.sh --NotebookApp.token=''`
      - Upload the and the '.ipynb' and the CSV data from the scraper directory through Jupyter's interface, or by mounting a volume with the correct files.
      - If you upload through the interface, Copy files out of container using `docker cp <containerId>:/file/path/within/container       /host/path/target`. If you mount a volume into the container then you are okay.
      -manipulate which model you want to use to generate bracker by changing the model used in "evaluate_winner" function to one of the previous models used in the notebook.
      - If your python kernels keep dying increase the Memory allowed for docker containers in Docker > Settings
  
  ## Results 
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
    - Take in game locations and team locations to calculate travel distance as a feature for both teams
    - Remove outliers, or incorrect values (- when supposed to be +)
  - Look into using Tensor flow or Pytorch for using Neural networks
  - Improve method for prediction
    - Use Evolutionary method to optimize hyper-parameters (learning rate batch size)
    - Predict both team scores instead of outcome?
    - Boost low seed stats if they beat a high seed, reduce high seed stats if they have close game with lower seed
    
  
    
