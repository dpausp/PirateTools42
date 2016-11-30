# -*- coding: utf-8 -*-
'''
eventsync.redmine.localsettings.py
Created on 15.03.2013
@author: escaP
'''

#API_KEY = "8f59fcc6e90472a998a93693d30cdf79c8d97559" # user escaP
# API_KEY = "50d0ce513487761ad06d20b000abc4495d6de7df" # user redmine_event_sync
API_KEY = "9d35ff3f67f2c90714b21e7d1ff90fd4e76aa4e7" # user escap_admin
REDMINE_SCHEMA = "https"
REDMINE_HOST = "redmine.piratenpartei-bayern.de"
API_SITE = "https://{}@{}".format(API_KEY, REDMINE_HOST)
REDMINE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
REDMINE_DATE_FORMAT = "%Y-%m-%d"
REDMINE_TIME_FORMAT = "%H:%M:%S"
READABLE_DATE_FORMAT = "%d.%m.%Y"
READABLE_TIME_FORMAT = "%H:%M"