#!/usr/bin/python2.6

import json

from BeautifulSoup import BeautifulSoup
import urllib2

delicious_username = "blech"

network_url = "http://feeds.delicious.com/v2/json/networkmembers/%s" % delicious_username
network_json = urllib2.urlopen(network_url).read()

network = json.loads(network_json)

for user in network:
  pinboard_url = "http://pinboard.in/u:%s" % user['user']
  
  page = urllib2.urlopen(pinboard_url)
  if page.geturl() != pinboard_url:
    print "  User %s not found under that name" % user['user']
    continue
  
  print pinboard_url