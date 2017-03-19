from __future__ import print_function
import sys

def console_print(string):
    print(string, file=sys.stderr)

def time_list():
    timeList = []
    for i in range(0, 4*24):
        if (i % 4) * 15 == 0:
            timeList.append(str(i / 4) + ":00")
        else:
            timeList.append(str(i / 4) + ":" + str((i % 4) * 15))
    return timeList

def weekday_list():
    weekdayList = []
    weekdayList.append('Monday')
    weekdayList.append('Tuesday')
    weekdayList.append('Wednesday')
    weekdayList.append('Thursday')
    weekdayList.append('Friday')
    weekdayList.append('Saturday')
    weekdayList.append('Sunday')
    return weekdayList

def example_function():
    return "return value"
