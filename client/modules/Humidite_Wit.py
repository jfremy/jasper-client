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
        print "has getentities"
        entities = text.getentities()
        print entities
        if 'location' in entities:
            for (feed, regex) in LOCATIONS:
                print "trying " + feed
                if re.search(regex, entities['location'][0]['value'], re.IGNORECASE):
                    print "regex " + regex + " has matched"
                    feedname = feed
                    location = entities['location'][0]['value']
                    break

    locname = "humidite_" + feedname

    if locname in profile['opensense']['feeds']:
        value = opensense.getlatestevent(profile, profile['opensense']['feeds'][locname])
        mic.say(u'The humidity in %s is %s%%' % (location, value))
    else:
        mic.say(u'Unknown location')



def isValid(text):
    return bool(re.search(r'\bdemande_humidite\b', text, re.IGNORECASE))
