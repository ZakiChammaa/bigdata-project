# bigdata-project
## Prepare Environment
* Clone project:

  ```bash
  git clone git@github.com:ZakiChammaa/bigdata-project.git
  ```
* Create a virtual environment:

  ```bash
  virtualenv -p python3 virtualenv
  ```
* Install the required libraries:
  
  ```bash
  pip install -r requirements.txt
  ```
## How to run
* Build machine learning model:
  
  You can build the decision tree or the random forest model. Note that you have to delete the model/ directory everytime you want to build a new one.<br><br>
  To build the decision tree model:
  ```bash
  python ml/decision_trees.py
  ```
  To build the random forest model:
  ```bash
  python ml/random_forest.py
  ```
* Stream the data and evaluate:

  To stream the data, open 2 terminals.<br><br>
  On the first one, run the following:
  ```bash
  python server.py localhost 9999
  ```
  On the second terminal, run the following:
  ```bash
  ./virtualenv/bin/spark-submit streaming.py localhost 9999
  ```
  When the data is done streaming, kill the program and run the following to get the accuracy:
  ```bash
  python test_accuracy.py
  ```

Note that the data is already cleaned up and is available in the data folder. If you want to run the preprocessing script, run the following:


```bash
python data_preprocessing.py
```
