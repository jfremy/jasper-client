# -*- coding: utf-8-*-
import urllib2
import json
import re
from client import opensense

WORDS = []

def handle(text, mic, profile):
    value = opensense.getlatestevent(profile, profile['opensense']['feeds']['consommation'])
    mic.say(u'The power consumption is %s watts' % value)

def isValid(text):
    return bool(re.search(r'\bdemande_conso\b', text, re.IGNORECASE))
