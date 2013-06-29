#!/usr/bin/python -tt
import sys
from matplotlib import pyplot as plt
import utils

def main():

  if len(sys.argv) != 3:
    print 'Usage:\t./data_viz.py TICKER_SYMBOL PREVIOUS_DAYS'
    print 'eg:\t./data_viz.py NFLX 365'

  D = utils.load_data('i30/stocks/' + sys.argv[1] + '.csv')[-1*int(sys.argv[2]):]

  x = range(len(D))

  # find closing prices for days
  # divide by average to scale down to see timestep_transform data
  y = [d[-2] for d in D]
  y_avg = sum(y)/len(y)
  y = [num/y_avg for num in y]
  
  X, labels = utils.timestep_transform(D, 10)
  
  
  plt.plot(x, y)
  plt.plot(range(10, len(labels)+10), labels)
  plt.show()


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

