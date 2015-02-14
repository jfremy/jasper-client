# -*- coding: utf-8-*-
import urllib2
import json
import re

WORDS = []

def handle(text, mic, profile):
    URL = 'http://api.sen.se/feeds/%s/last_event/?sense_key=%s' % (profile['opensense']['feeds']['consommation'], profile['opensense']['key'])
    req = urllib2.Request(URL)
    resp = urllib2.urlopen(req)
    data = json.load(resp)
    print data
    mic.say('La consommation électrique courante est %s watts' % data['value'])

def isValid(text):
    return bool(re.search(r'\bdemande_conso\b', text, re.IGNORECASE))
