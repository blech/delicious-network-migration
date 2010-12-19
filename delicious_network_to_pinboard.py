#!/usr/bin/python2.6

import json

from BeautifulSoup import BeautifulSoup
import urllib
import urllib2

delicious_username = "blech"

pinboard_username = "blech"
pinboard_password = ""

# get the network (hurrah for the delicious v2 api; why have I not used it?)

network_url = "http://feeds.delicious.com/v2/json/networkmembers/%s" % delicious_username
network_json = urllib2.urlopen(network_url).read()

network = json.loads(network_json)

# get the delpin mapping file for non-identical usernames and turn it
# into a hash

mapping_url = "http://delpin.heroku.com/export.json?different=true"
mapping_json = urllib2.urlopen(mapping_url).read()

mapping = json.loads(mapping_json)

mapping_hash = {}

for row in mapping:
  mapping_hash[row['delicious'].lower()] = row['pinboard']  

# construct cookie-based URL opener so we can go crazy with subscribe buttons

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
urllib2.install_opener(opener)

# authenticate with pinboard_password
params = urllib.urlencode(dict(username=pinboard_username, password=pinboard_password))
f = opener.open('http://pinboard.in/auth/', params)
# TODO check this actually logs you in (look for variant page details?)
f.close()


for user in network:
  # note that 'user' is a hash of data from Delicious, while
  # 'username' is the (probable) Pinboard username of that user
  # I should have used better variable names really...

  # does the mapping file know about them?

  try:
    mapping_hash[user['user'].lower()]
    username = mapping_hash[user['user'].lower()]
  except Exception, e:
    username = user['user']

  # TODO point out when a variant mapping is used?
  pinboard_url = "http://pinboard.in/u:%s" % username
  
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
        # TODO keep a list of who this has subscribed to so you can
        # go back and check it later

      else:
        print "  Not OK: something went wrong"
      
      result.close()

    else:
      
      print "  Already subscribed"

    # break

  else:  
  
    print "  User %s not found" % username
