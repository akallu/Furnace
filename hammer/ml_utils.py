#!/usr/bin/python -tt
import re
import sys
import cPickle as pickle
import sklearn as sk


'''
GIVEN:
	non-normalized training data, X and assoc. labels, y
	
	optional parameter tuple to specify:
		kernel function
		margin
		gamma (depending on if RBF function used)

RETURN:
	SVM model tuned using grid search and cross validation
	scaler object to scale (normalize) future test data
''' 
def generate_model(X, y, params=None, param_grid=None):

  #if grid_params was not specified, let us specify them
  if param_grid == None:
    #grid space intentionally kept small for performance issues
    C = [-1, 0, 1, 3]
    G = [-3, -1, 0, 1]

    C = [10**c for c in C]
    G = [10**g for g in G]

    param_grid = [
	{'C': C, 'kernel': ['linear']},
	{'C': C, 'gamma': G, 'kernel': ['rbf']},
	]

  # generate scaler so that we may scale any future test data
  scaler = sk.preprocessing.StandardScaler().fit(X)

  # generate base model to pass to grid search
  # here we use support vector regression for real valued classification
  base_model = sk.svm.SVR()

  # load in model and params for grid search
  # n_jobs=-1 tells it to run computations in parallel 
  model = sk.grid_search.GridSearchCV(base_model, param_grid, n_jobs=-1)
  
  # fit our training data
  model.fit(scaler.transform(X), y)

  print 'Best parameters found:', model.best_params_
  print 'Best score:', model.best_score_

  return (model, scaler)
  


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

