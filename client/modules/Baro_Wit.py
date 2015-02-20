# -*- coding: utf-8-*-
import urllib2
import json
import re
from client import opensense

WORDS = []

def handle(text, mic, profile):
    value = opensense.getlatestevent(profile, profile['opensense']['feeds']['pression'])
    mic.say(u'The atmospheric pressure is %s bars' % value)

def isValid(text):
    return bool(re.search(r'\bdemande_baro\b', text, re.IGNORECASE))
