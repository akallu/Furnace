#!/usr/bin/python -tt
import sys
from matplotlib import pyplot as plt
import utils
import sklearn as sk
import math

def main():
  D = utils.load_data('i30/stocks/NFLX.csv')
  train = D[-500:]
  test = D[-100:]
  X_train, y_train = utils.timestep_transform(train, 10)
  X_test, y_test = utils.timestep_transform(test, 10)
  model, scaler = utils.generate_model(X_train, y_train)
  X_test = scaler.transform(X_test)
  pred_vals = model.predict(X_test).tolist()

  #plt.plot(range(len(y_test)), y_test)
  #plt.plot(range(len(pred_vals)), pred_vals)

  diff = [y_test[i]-pred_vals[i] for i in xrange(len(y_test))]
  plt.plot(range(len(diff)), diff)
  
  plt.show()


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

