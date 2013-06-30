#!/usr/bin/python -tt
import sys
from matplotlib import pyplot as plt
import utils
import sklearn as sk
import math

def main():
  if len(sys.argv) != 2:
    print 'Usage:\t./benchmark.py TICKER_SYMBOL'
    print 'Ex:\t./benchmark.py NFLX'
    sys.exit()


  k = 10

  D = utils.load_data('i30/stocks/' + sys.argv[1] + '.csv')
  train = D[-500:-100]
  test = D[-100:]
  X_train, y_train = utils.timestep_transform(train, k)
  X_test, y_test = utils.timestep_transform(test, k)
  model, scaler = utils.generate_model(X_train, y_train)
  X_test = scaler.transform(X_test)
  pred_vals = model.predict(X_test).tolist()

  #plt.plot(range(len(y_test)), y_test)
  #plt.plot(range(len(pred_vals)), pred_vals)

  #diff = [y_test[i]-pred_vals[i] for i in xrange(len(y_test))]
  #plt.plot(range(len(diff)), diff)
  
  #set of test data closing prices
  C = [t[-2] for t in test[k-1:]]

  #our predvals is the percent change a day will undergo the day after
  C_ = [pred_vals[i]*C[i] for i in xrange(len(C)-1)]
  C = C[:-1]

  print len(C)
  print len(C_)

  plt.plot(range(len(C)), C)
  plt.plot(range(len(C_)), C_)

  plt.show()


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

