#!/usr/bin/python -tt
import re
import sys
sys.path.append('../SWAG/code/')
import classifiers as cl
import meta_classifiers as mcl
import cPickle as pickle
import math

def main():
  D = get_data('i30/stocks/nflx.csv')
  T, E = split_data(D, int(len(D)*.8))

  C_svm = cl.SVM(T, kernel_type='RBF', margin=1, gamma=8)
  #C_knn = cl.kNN(T)
  
  benchmark(C_svm, E)
  #benchmark(C_knn, E)

#C is classifier, E is test data
def benchmark(C, E):
  correct = 0.0
  for e in E:
    if C.classify_vector(e) == e[-1]:
      correct += 1.0
  print C.get_info()
  print 'Test Accuracy:\n\t', correct/len(E)

def get_data(filename, prev_days=5):
  lines = open(filename, 'r').read().strip().split('\n')
  D = []
  for line in lines[1:]:
    raw = line.strip().split(',')
    date = raw[0].strip().split('-')
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    
    D.append( [date_to_day(year, month, day)] + [float(val) for val in raw[1:]] )

  F = []

  avg_diff = 0.0
  total = 0
  #we construct feature vectors based on (n - prev_days) days
  for i in xrange(len(D) - (prev_days + 1)):
    #D[i][-1] refers to adjusted closing price for day i
    norm_diff = norm(D[i][-1], D[i+1][-1])
    avg_diff += norm_diff
    total += 1
    if norm_diff > 0:
      label = 1
    else:
      label = 0

    #feature one is the day of the week
    f = [D[i][0]]
   
    #features are going to be fluctuation of previous five days
    for j in xrange(i+1, i+prev_days):
      f.append(norm(D[j][-1], D[j+1][-1]))
    f.append(label)
    F.append(f)
  print avg_diff/total
  return F
    



def norm(a, b):
  return (b-a)/a



#takes in tuple of form (year, month number, day number) and gives
#the day of the week in number form, 0 for sunday, 1 for monday, ...
def date_to_day(year, month_num, day_num):

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


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

