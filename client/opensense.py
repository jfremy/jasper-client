# -*- coding: utf-8-*-
import requests


def getlatestevent(profile, feedid):
    try:
        apikey = profile['opensense']['key']
        url = 'http://api.sen.se/feeds/%s/last_event/?sense_key=%s' % (feedid, apikey)
        req = requests.get(url)
        req.raise_for_status()
        data = req.json()
        print(data)
        result = data["value"]
    except requests.exceptions.HTTPError:
        return ""
    except requests.exceptions.RequestException:
        return ""
    except ValueError:
        return ""
    except KeyError:
        return ""
    else:
        return result