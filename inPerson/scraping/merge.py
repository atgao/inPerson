"""
Python routine to format json to put into database. Code adapted
from ClassMaps routine (COS333 S18).
by Alice Gao '21
"""
import sys
import json
import copy
from datetime import datetime
import re

# Convert into a form that can be put into the database
def convert_db(data, project, model):
    pk=1
    ret = []
    for ent in data:
        temp = {}
        temp['pk'] = pk
        temp['model'] = project+"."+model
        temp['fields'] = ent
        ret.append(temp)
        pk+=1
    return ret

with open('courses.json') as handle:
    course_info = json.load(handle)

converted = convert_db(course_info, "schedule", "section")

with open('course_data.json', 'w') as handle:
    json.dump(converted, handle)
