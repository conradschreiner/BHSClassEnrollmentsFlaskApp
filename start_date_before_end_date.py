
'''
Citation Scope: function start_date_before_end_date
Date: 3/17/25
Originality: Based on the example in the following source, Iris converted start and end date strings into datetime objects via strptime function from datetime class of datetime module and compared them with a comparison operator
Source: https://stackoverflow.com/questions/60701379/how-to-compare-dates-in-python-and-find-the-greater-one
'''
import datetime

def start_date_before_end_date(start, end):
  start_date_datetime_object = datetime.datetime.strptime(start, '%Y-%m-%d')
  end_date_datetime_object = datetime.datetime.strptime(end, '%Y-%m-%d')
  if start_date_datetime_object < end_date_datetime_object:
    return True
  return False