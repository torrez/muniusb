#!/usr/bin/env python3

from subprocess import call
import xml.etree.ElementTree as ET
import time

import requests

"""
You’ll need a blink1 http://blink1.thingm.com/ attached to a USB port.
If you have more than one you’ll have to pass the id of the one you want
to use to the blink1-tool command. You’ll also need the blink1-tool
command installed in your path.

Next you need to find your MUNI stop. Go here to get the list of routes:
    http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=sf-muni
Then go here to get your stopId:
    http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r=<routeTag>
Then construct your query with this:
http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&stopId=<stopId>&routeTag=<routeTag>

Finally, determine your fast_walk and slow_walk times, meaning if there
is a train due to your stop between your fast and slow walk times, then
you have a chance to make it.
"""

stop_url_request = ("http://webservices.nextbus.com/service/publicXMLFeed"
                    "?command=predictions&a=sf-muni&stopId=16995&routeTag=N")
fast_walk = 5
slow_walk = 8
blink1_cmd = "/usr/local/bin/blink1-tool"

r = requests.get(stop_url_request)
root = ET.fromstring(r.text)

list_of_departures = []

for neighbor in root.iter('prediction'):
    list_of_departures.append(neighbor.attrib['minutes'])

for departure in list_of_departures:
    departure = int(departure)
    if fast_walk < departure < slow_walk:
        call([blink1_cmd, "--rgb=0,100,0"])
        break
    else:
        call([blink1_cmd, "--rgb=100,0,0"])
