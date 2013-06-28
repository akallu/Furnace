#!/usr/bin/python -tt
import re
import sys
import cPickle as pickle
import math

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
      if not 'nan' in vals:
        #first entry is date string, leave it intact
        vals = vals[0] + [float(val) for val in vals[1:]]
        D.append(vals)

  return D


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

