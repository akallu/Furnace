#!/usr/bin/python -tt
import sys
import numpy as np
import Quandl as q

def main():

  # user should specify one argument only
  if len(sys.argv) != 2:
    print 'Usage: ./ticker_data.py INDEX_TICKER'
    print 'Example: ./ticker_data.py NASDAQ_NFLX'
    sys.exit()

  #auth token for akallu
  auth_token = 'DvtyfczL4jNaGzWwqRZ3'
  
  # first argument should be ticker symbol as such:
  # NASDAQ_NFLX
  ticker_symbol = sys.argv[1]
  
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

