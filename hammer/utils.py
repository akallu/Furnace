#!/usr/bin/python -tt
import re
import sys
import cPickle as pickle
import sklearn as sk
from sklearn import preprocessing, svm, grid_search
import numpy as np

#gives day of the week in number form, 0 for sunday, 1 for monday, ...
def day_of_week(year, month_num, day_num):

  month_table = [0, 3, 3, 6, 1, 4, 6, 2, 5, 0, 3, 5]
  if is_leap_year(year):
    month_table[0] = -1
    month_table[1] = 2
  
  return (day_num + month_table[month_num-1] + year%100 + int((year%100)/4.0) + 6) % 7

def is_leap_year(year):
  if year % 400 ==0:
    return True
  elif year % 100 == 0:
    return False
  elif year % 4 == 0:
    return True
  else:
    return False

def split_data(data, lim):
  return (data[:lim], data[lim:])


def load_data(filename):
  D = []
  with open(filename, 'r') as f:
    #advance past header
    f.next()
    for line in f:
      vals = line.strip().split(',')
      #we ignore any days that have NaN entries
      if (not 'nan' in vals) and len(line.strip()) > 1:
        #first entry is date string, leave it intact
        #also check for empty strings in vals
        vals = [vals[0]] + [float(val) for val in vals[1:] if len(val) > 0]
        D.append(vals)

  return D


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
  X = np.asarray(X)
  y = np.asarray(y)

  # generate scaler so that we may scale any future test data
  scaler = preprocessing.StandardScaler().fit(X)

  # if grid_params and params were not specified, let us specify grid_params
  if param_grid == None and params == None:
    # grid space intentionally kept small for performance issues
    C = [0, 1, 3]
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
    base_model = svm.SVR(cache_size=1000)

    # load in model and params for grid search
    # n_jobs=-1 tells it to run computations in parallel 
    model = grid_search.GridSearchCV(base_model, param_grid)
  
    # fit our training data
    model.fit(scaler.transform(X), y)

    #print 'Best parameters found:', model.best_params_
    #print 'Best score:', model.best_score_
  
  # params were specified, so simply train model using these params
  else:
    #we set cache size to 1000 MB
    if params['kernel'] == 'linear':
      model = svm.SVR(kernel='linear',
			C=params['C'],
			cache_size=1000)
    elif params['kernel'] == 'rbf':
      model = svm.SVR(kernel='rbf',
			C = params['C'],
			gamma = params['gamma'],
			cache_size = 1000)
    else:
      raise ValueError('Please specify kernel as either linear or rbf')
      sys.exit() 

  return (model, scaler)



'''
GIVEN:
	raw data, D, given by quandl in form of:
	    day_1 = [date_string_1, open_1, high_1, low_1, close_1, volume_1]
					...
					...
					...
	    day_n = [date_string_n, open_n, high_n, low_n, close_n, volume_n]

	timeframe window limit, k

RETURN:
    transformed data, X and labels y in form:
        X_k = [close_k-1 / close_k-2, ..., close_2 / close_1, day_of_week] y_k = close_k / close_k-1
						...
						...
						...
	X_n = [close_n-1 / close_n-2, ..., close_n-k+1 / close_n-k, day_of_week] y_n = close_n / close_n-1
'''
def timestep_transform(D, k):
  X = []
  y = []
  for i in xrange(k, len(D)):
   
    year_, month_, day_ = parse_datestring(D[i][0])
    X_i = [D[i-j][-2] / D[i-j-1][-2] for j in xrange(1, k+1)] + [D[i-j][-1] / D[i-j-1][-1] for j in xrange(1, k+1)]  + [day_of_week(year_, month_, day_)]
    y_i = D[i][-2] / D[i-1][-2]
    X.append(X_i)
    y.append(y_i)

  return (X, y)


#essentially the same thing as timestep, but transforms the current day
#into attributes for prediction purposes
def day_transform(D, k):
  #let i be the last element in D (the current day) 
  i = len(D)-1

  year_, month_, day_ = parse_datestring(D[i][0])
  #print year_, month_, day_
  x = [D[i-j][-2] / D[i-j-1][-2] for j in xrange(k)] + [D[i-j][-1] / D[i-j-1][-1] for j in xrange(k)]  + [day_of_week(year_, month_, day_)]

  return x

'''
GIVEN:
    date string, s, in form:
      'YYYY-MM-DD'

RETURN:
    tuple of ints in form:
      (year, month, day)
    
'''
def parse_datestring(s):
  s = s.strip().split('-')
  return (int(s[0]), int(s[1]), int(s[2]))


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

