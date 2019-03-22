## Updating the Database Outline
---
## Requirements
It is strongly recommended, though not strictly necessary, to create a new environment with virtualenv or a similar tool.

### Updating Database
1. Python 3
2. Django 2.1
3. PostgreSQL 11

## Introduction
Course data is scraped from OIT webfeeds using the script in ../scraping/
directory. All future filepaths will be relative to this folder. The data
is then moved into a Heroku hosted postgres database with the following steps:
1. Scrape the raw data and format as a json file
2. Process raw data into another json file
3. Add this json to Heroku database

## Scrape the Raw Data
Course data is saved to courses.json by running:
python scraper.py > courses.json

For each course, the sections, meeting times, and building locations are
retrieved.

## Process the Data
This data must now be cleaned so it can be loaded into the Heroku database. This
is done by running:
python merge.py
which formats the data into course_data.json

## Add json to Heroku Database
Navigating to the root direct of the project, the following command is run
python manage.py loaddata scraping/course_data.json 
