#!/usr/bin/python2.6

import json

from BeautifulSoup import BeautifulSoup
import urllib
import urllib2

delicious_username = "blech"

pinboard_username = "blech"
pinboard_password = ""

network_url = "http://feeds.delicious.com/v2/json/networkmembers/%s" % delicious_username
network_json = urllib2.urlopen(network_url).read()

network = json.loads(network_json)

# construct cookie-based URL opener so we can go crazy with subscribe buttons

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
urllib2.install_opener(opener)

# authenticate with pinboard_password
params = urllib.urlencode(dict(username=pinboard_username, password=pinboard_password))
f = opener.open('http://pinboard.in/auth/', params)
f.close()

for user in network:
  pinboard_url = "http://pinboard.in/u:%s" % user['user']
  
  page = urllib2.urlopen(pinboard_url)
  if page.geturl() == pinboard_url:
    print pinboard_url

    soup = BeautifulSoup(page)
    
    # subscription: if the subscribe link is not display:none, then
    # we can POST to /subscribe/ with the username and a the 
    # CSRF token (which we can fetch from the onclick parameters)
    
    sub_div = soup.findAll('div', { 'class': 'subscribe_link' })
        
    if sub_div[0]['style'] == "display:block;":

      links = sub_div[0].findAllNext('a')
      js = links[0]['onclick']
      arguments = js[js.index('(')+1:js.index(')')]
      username, token = arguments.split(',')
      username = username.strip("'")
      token = token.strip("'")

      # print "  Need to click subscribe button for %s" % (user)

      params = urllib.urlencode(dict(username=username, token=token))
      result = opener.open('http://pinboard.in/subscribe/', params)
      if result.read() == "['ok']":
        print "  Subscribed"
      else:
        print "  Not OK: something went wrong"
      
      result.close()

    else:
      
      print "  Already subscribed"

    # break

  else:  
  
    print "  User %s not found under that name" % user['user']
    # TODO use the delpin username mapping JSON file
    # actually, we should do that before even firing the GET...
