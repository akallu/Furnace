#!/usr/bin/python -tt
import sys
from matplotlib import pyplot as plt
import utils
import math

def main():

  if len(sys.argv) != 3:
    print 'Usage:\t./data_viz.py TICKER_SYMBOL PREVIOUS_DAYS'
    print 'Ex:\t./data_viz.py NFLX 365'
    sys.exit()

  D = utils.load_data('i30/stocks/' + sys.argv[1] + '.csv')[-1*int(sys.argv[2]):]

  #first we find closing prices, and then divide by average
  #divide by average to scale data down and still preserve the shape of trend
  C = [d[-2] for d in D]
  avg_close = sum(C) / len(C)
  C = [c / avg_close for c in C]

  #same as above, but with trading volumes instead
  V = [d[-1] for d in D]
  avg_vol = sum(V) / len(V)
  V = [v / avg_vol for v in V]

  #construct relative changes
  rel_C = rel_change(D, -2)
  rel_V = rel_change(D, -1)

  #non-relative stock data
  plt.plot(range(len(D)), C)
  #plt.plot(range(len(D)), V)

  #relative stock data
  #plt.plot(range(1, len(D)), rel_C)
  #plt.plot(range(1, len(D)), rel_V)


  #to see correlation between rel_C and rel_V
  alpha = 5.55
  X = [ alpha*(abs(1-rel_C[i]) / rel_V[i]) for i in xrange(len(rel_C))]

  plt.plot(range(1, len(D)), X)

  plt.show()

#specify index of variable you want to choose
#outputs list relative change from a day and previous day
def rel_change(D, index):
  return [D[i][index] / D[i-1][index] for i in xrange(1, len(D))]

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

