#!/usr/bin/python -tt
import sys
import numpy as np
import Quandl as q

def main():

  nsdq = ['AAPL', 'ALGN', 'ATML', 'CAR', 'CIEN', 'CTXS', 'GOOG', 'NFLX', 'SBGI',
	'SIRI', 'STX']
  nyse = ['APC', 'BC', 'BID', 'BKD', 'BX', 'CBG', 'DAN', 'DDD', 'FCX', 'FNP',
	'HIG', 'IPG', 'LYB', 'MGM', 'MS', 'OI', 'RCL', 'RF', 'THO', 'TPX', 'VLO']

  for t in nsdq:
    get_ticker_data('NASDAQ_'+t)

  for t in nyse:
    get_ticker_data('NYSE_'+t)

def get_ticker_data(ticker_symbol):
  #auth token for akallu
  auth_token = 'DvtyfczL4jNaGzWwqRZ3'
  
  # first argument should be ticker symbol as such:
  # NASDAQ_NFLX
  
  #return data as numpy array
  data = q.get('GOOG/' + ticker_symbol,
		authtoken = auth_token, 
		collapse='daily',
		returns='numpy').tolist()
  
  #cache data in i30/stocks/
  with open('i30/stocks/' + ticker_symbol.split('_')[-1] + '.csv', 'w') as f:
    f.write('DATE,OPEN,HIGH,LOW,CLOSE,VOLUME\n')
    for line in data:
      for val in line:
        f.write(str(val) + ',')
      f.write('\n')

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

