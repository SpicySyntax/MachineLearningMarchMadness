# MachineLearningMarchMadness
Predictive solution for March Madness bracket
Description: 
  - Try to predict the NCAA tournament bracket. Scrape data from the web and used ML to predict the outcomes of games
Components:
  - Web Scraper:
    - uses Python 2.7.14,
    - use 'pip' to install csv and selenium for the web scraper,
  - Notebook:
    - uses jupyter-notebooks via docker containers (see : https://hub.docker.com/r/jupyter/datascience-notebook/ for details) 
      - If you don't have docker installed, install it (I used docker for windows)
      - To run I used: docker run -d -p 8888:8888 jupyter/datascience-notebook start-notebook.sh --NotebookApp.token='' (No auth)
      - Upload the and the '.ipynb' and the CSV data from the scraper directory through Jupyter's interface, or by mounting a volume with the       correct files.
      - If you upload through the interface, Copy files out of container using "docker cp <containerId>:/file/path/within/container       /host/path/target". If you mount a volume into the container then you are okay.
      -manipulate which model you want to use to generate bracker by changing the model used in "evaluate_winner" function to one of the previous models used in the notebook.

