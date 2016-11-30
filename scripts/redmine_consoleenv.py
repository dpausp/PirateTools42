# -*- coding: utf-8 -*-
'''
.py
Created on 15.03.2013
@author: escaP
'''
from __future__ import division, absolute_import, print_function

from datetime import datetime
import logging
from imp import reload
import importlib
import sys

sys.path.append(".")

from dateutil.relativedelta import relativedelta
from piratetools42.redmineapi import *
    
q = s.query

print("Redmine Env")
