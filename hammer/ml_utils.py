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

  # generate scaler so that we may scale any future test data
  scaler = sk.preprocessing.StandardScaler().fit(X)

  # if grid_params and params were not specified, let us specify grid_params
  if param_grid == None and params == None:
    # grid space intentionally kept small for performance issues
    C = [-1, 0, 1, 3]
    G = [-3, -1, 0, 1]

    C = [10**c for c in C]
    G = [10**g for g in G]

    param_grid = [
	{'C': C, 'kernel': ['linear']},
	{'C': C, 'gamma': G, 'kernel': ['rbf']},
	]

  # no params were specified, so perform grid search
  if params == None:
    # generate base model to pass to grid search
    # here we use support vector regression for real valued classification
    # cache_size is cache size in MB
    base_model = sk.svm.SVR(cache_size=1000)

    # load in model and params for grid search
    # n_jobs=-1 tells it to run computations in parallel 
    model = sk.grid_search.GridSearchCV(base_model, param_grid, n_jobs=-1)
  
    # fit our training data
    model.fit(scaler.transform(X), y)

    print 'Best parameters found:', model.best_params_
    print 'Best score:', model.best_score_
  
  # params were specified, so simply train model using these params
  else:
    #we set cache size to 1000 MB
    if params['kernel'] == 'linear':
      model = sk.svm.SVR(kernel='linear',
			C=params['C'],
			cache_size=1000)
    elif params['kernel'] == 'rbf':
      model = sk.svm.SVR(kernel='rbf',
			C = params['C'],
			gamma = params['gamma'],
			cache_size = 1000)
    else:
      raise ValueError('Please specify kernel as either linear or rbf')
      sys.exit()
   

  return (model, scaler)
  


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

