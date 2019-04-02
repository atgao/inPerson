#!/usr/bin/env python
"""
Python routine for scraping course data from Princeton's OIT webfeeds.
by Alice Gao '21.
"""

from datetime import datetime
import json
import re
import string
import sqlite3
import sys
import requests
from bs4 import BeautifulSoup

TERM_CODE = 1122  # seems to be fall 11-12
TERM_CODE = 1124  # so 1124 would be spring 11-12
                  # 1134 is definitely spring 13 (course offerings link)`
TERM_CODE = 1134
TERM_CODE = 1142  # fall 2013; spring 2014 will be 1144
TERM_CODE = 1144  # spring 2014
TERM_CODE = 1154  # spring 2015
TERM_CODE = 1174  # spring 2017
TERM_CODE = 1184  # spring 2018
TERM_CODE = 1182  # fall 2017 ??
TERM_CODE = 1194  # spring 2019

URL_PREFIX = "http://etcweb.princeton.edu/webfeeds/courseofferings/"
LIST_URL = URL_PREFIX + "?fmt=json&term={term}&subject=all"
DEFAULT_TIME = "00:00"

data = []
TERM_SUFFIX = ""

# format time into date time object
def format_time(time):
    if time == "":
        return DEFAULT_TIME
    else:
        return datetime.strptime(time, "%I:%M %p").strftime("%H:%M")

# helper function to merge two dictionaries
# returns new merged dictionary
def merge(dict1, dict2):
    res = {**dict1, **dict2}
    return rest

def get_data():
    WEBFEED_URL = LIST_URL.format(term=TERM_CODE)
    global data
    data = requests.get(WEBFEED_URL).json()['term'][0]['subjects']
    global TERM_SUFFIX
    TERM_SUFFIX = requests.get(WEBFEED_URL).json()['term'][0]['suffix']

# helper function to get start time, end time, loc and days of a class
# returns a dictionary of {start_time, end_time, days, location}
def get_course_details(classes):
    meetings = classes['schedule']['meetings'][0]
    start_time = format_time(meetings['start_time'])
    end_time = format_time(meetings['end_time'])
    days_of_week = []
    location = ""
    if "days" in meetings: # this does not exist for all classes
        days_of_week = meetings["days"]
    if "building" in meetings: # this does not exist for all classes
        location = "{} {}".format(meetings["building"]["building_code"], meetings["room"])

    return {
        'start_time': start_time,
        'end_time': end_time,
        'days': days_of_week,
        'location': location
    }


# get all sections of a course
def get_section(data):
    courses = []
    global TERM_SUFFIX
    for dept in data:
        code = dept['code']

        for course in dept['courses']:
            title = course['title']
            catalog_number = course['catalog_number']

            for classes in course['classes']:
                if classes['status'] == "Cancelled": # must skip cancelled sections since registrar keeps them
                    break
                class_number = classes['class_number']
                section = classes['section']
                details = get_course_details(classes)
                dict = {'term': TERM_SUFFIX, 'class_number': class_number, 'code': code,
                'catalog_number': catalog_number, 'title': title, 'section': section}
                dict.update(details) # merge the two dictionaries into dict
                courses.append(dict)
    return courses

if __name__ == '__main__':
    get_data()
    sections = get_section(data)
    first = True
    for section in sections:
        if first:
            first = False
            print('[')
        else:
            print(',')
        json.dump(section, sys.stdout)
    print(']')
