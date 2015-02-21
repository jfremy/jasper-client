# -*- coding: utf-8-*-
import re
from client import opensense

WORDS = []
LOCATIONS = [
    ('chambre', r'\bchambre\b'),
    ('bureau', r'\bbureau\b'),
    ('salle_de_bain', r'\bsalle de bain\b'),
    ('salon', r'\bsalon\b'),
    ('balcon', r'\bdehors|balcon\b')
]


def handle(text, mic, profile):
    location = 'balcon'
    feedname = 'balcon'
    if hasattr(text, "getentities"):
        entities = text.getentities()
        if 'location' in entities:
            for (feed, regex) in LOCATIONS:
                print "trying " + feed
                if re.search(regex, entities['location'][0]['value'], re.IGNORECASE):
                    print "regex " + regex + " has matched"
                    feedname = feed
                    location = entities['location'][0]['value']
                    break

    locname = "temperature_" + feedname

    if locname in profile['opensense']['feeds']:
        value = opensense.getlatestevent(profile, profile['opensense']['feeds'][locname])
        mic.say(u'Temperature in %s is %s Celsius' % (location, value))
    else:
        mic.say(u'Unkown location')



def isValid(text):
    return bool(re.search(r'\bdemande_temperature\b', text, re.IGNORECASE))
