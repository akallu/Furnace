#!/usr/bin/python -tt
import sys
from matplotlib import pyplot as plt
import utils
import sklearn as sk
import math
import datetime

def main():
  nsdq = ['AAPL', 'ALGN', 'ATML', 'CAR', 'CIEN', 'CTXS', 'GOOG', 'NFLX', 'SBGI',
        'SIRI', 'STX']
  nyse = ['APC', 'BC', 'BID', 'BKD', 'BX', 'CBG', 'DAN', 'DDD', 'FCX', 'FNP',
        'HIG', 'IPG', 'LYB', 'MGM', 'MS', 'OI', 'RCL', 'RF', 'THO', 'TPX', 'VLO']

  symbols = nsdq+nyse

  today = datetime.date.today()

  date_str = str(today.year) + '_' + str(today.month) + '_' + str(today.day)

  with open('i30/daily_predictions/' + date_str + '.csv', 'w') as f:
    f.write('TICKER_SYMBOL, PREV_CLOSE, NEXT_CLOSE, PROJECTED_CHANGE\n')
    for t in symbols:
      p_close, change, n_close = next_day_prediction(t)
      f.write(t + ', ' + str(p_close) + ', ' + str(n_close) + ', ' + str(change) + '\n')

def next_day_prediction(ticker_symbol):
  
  k = 10
  D = utils.load_data('i30/stocks/' + ticker_symbol + '.csv')
  #load in past year's data
  train = D[-365:]

  X_train, y_train = utils.timestep_transform(train, k)
  model, scaler = utils.generate_model(X_train, y_train)
  pred_val = model.predict(scaler.transform([utils.day_transform(D, k)])).tolist()
  
  curr_close = D[-1][-2]
  change = pred_val[0]-1
  next_close = pred_val[0]*curr_close

  '''
  print 'Current day closing value:'
  print '\t', curr_close

  print 'Projected change in closing value:'
  print '\t', 100*change

  print 'Project next day closing value:'
  print '\t', next_close
  '''

  return (curr_close, change, next_close)


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

