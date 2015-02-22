# -*- coding: utf-8-*-
import re
import requests

WORDS = []
UA = 'RATP/6.2.3 CFNetwork/711.1.16 Darwin/14.0.0'
SERVER = 'apixha.ixxi.net'

def handle(text, mic, profile):
    key = profile['ratp']['key']
    transports = profile['ratp']['types']

    selectedtransport = ''
    selectedline = ''
    selecteddirection = ''

    dirid = ''
    lineid = ''
    stopid = ''

    if hasattr(text, "getentities"):
        entities = text.getentities()
        print entities
        provtransport = ''
        if 'type' in entities:
            provtransport = entities['type'][0]['value']
            for conftransport in transports:
                if re.search(transports[conftransport]['regex'], provtransport, re.IGNORECASE):
                    selectedtransport = conftransport
                    break

        if selectedtransport == '':
            print entities
            mic.say("Unknown transportation type %s" % provtransport)
            return

        transport = transports[selectedtransport]
        lines = transport["lines"]

        provline = ''
        if 'line' in entities:
            provline = entities['line'][0]['value']
            for confline in lines:
                if re.search(lines[confline]['regex'], provline, re.IGNORECASE):
                    selectedline = confline
                    break

        if selectedline == '':
            print entities
            mic.say("Unknown line %s" % provline)
            return

        line = lines[selectedline]
        lineid = line["id"]
        directions = line["directions"]

        provdirection = ''
        if 'direction' in entities:
            provdirection = entities['direction'][0]['value']
            for confdirection in directions:
                if re.search(directions[confdirection]['regex'], provdirection, re.IGNORECASE):
                    selecteddirection = confdirection
                    break

        if selecteddirection == '':
            print entities
            mic.say("Unknown direction %s" % provdirection)
            return

        direction = directions[selecteddirection]
        stopid = direction["stop"]
        dirid = direction["id"]

        try:
            url = 'http://%s/APIX?keyapp=%s&withDetails=true&stopArea=%s&cmd=getNextStopsRealtime&apixFormat=json&line=%s&withText=true&direction=%s' % (SERVER, key, stopid, lineid, dirid)
            print "URL:", url
            req = requests.get(url, headers={"User-Agent": UA})
            req.raise_for_status()
            data = req.json()

            print(data)
            if ("nextStopsOnLines" in data) and ("nextStops" in data["nextStopsOnLines"][0]):
                nextStops = data["nextStopsOnLines"][0]["nextStops"]

                print nextStops
                lenstops = len(nextStops)
                if lenstops == 1:
                    if nextStops[0]["waitingTimeRaw"] == "SERVICE TERMINE":
                        mic.say("%s service for line %s is finished for today" % (transport["text"], line["text"]))
                    else:
                        mic.say("Next %s for line %s to %s is in %s" % (transport["text"], line["text"], direction["text"], nextStops[0]["waitingTimeRaw"].replace("mn", "minutes")))
                if lenstops >= 2:
                    if nextStops[0]["waitingTimeRaw"] == "SERVICE TERMINE":
                        mic.say("%s service for line %s to %s is finished for today" % (transport["text"], line["text"], direction["text"]))
                    else:
                        if nextStops[0]["waitingTimeRaw"] == "A l'approche":
                            mic.say("Next %s for line %s to %s is in %s" % (transport["text"], line["text"], direction["text"], nextStops[1]["waitingTimeRaw"].replace("mn", "minutes")))
                        else:
                            mic.say("Next %s for line %s to %s is in %s and the following is in %s" % (transport["text"], line["text"], direction["text"], nextStops[0]["waitingTimeRaw"].replace("mn", "minutes"), nextStops[1]["waitingTimeRaw"].replace("mn", "minutes")))
        except requests.exceptions.HTTPError as he:
            print "HTTPError ", he
        except requests.exceptions.RequestException as rex:
            print "RequestException ", rex
        except ValueError as ve:
            print "ValueError ", ve
        except KeyError as ke:
            print "KeyError ", ke
    else:
        mic.say("Oups")

def isValid(text):
    return bool(re.search(r'\bdemande_ratp\b', text, re.IGNORECASE))
