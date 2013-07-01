#!/usr/bin/python -tt
import sys
from matplotlib import pyplot as plt
import utils
import sklearn as sk
import math

def main():
  if len(sys.argv) != 2:
    print 'Usage:\t./next_day_prediction.py TICKER_SYMBOL'
    print 'Ex:\t./next_day_prediction.py NFLX'
    sys.exit()


  k = 10

  D = utils.load_data('i30/stocks/' + sys.argv[1] + '.csv')
  #load in past year's data
  train = D[-365:]

  X_train, y_train = utils.timestep_transform(train, k)
  model, scaler = utils.generate_model(X_train, y_train)
  pred_val = model.predict(scaler.transform([utils.day_transform(D, k)])).tolist()
  
  print 'Current day closing value:'
  print '\t', D[-1][-2]

  print 'Projected change in closing value:'
  print '\t', 100*(pred_val[0]-1)

  print 'Project next day closing value:'
  print '\t', pred_val[0]*D[-1][-2]

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

