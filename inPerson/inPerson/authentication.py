from django.contrib.auth.models import User # this line should be changed to reflect custom user
from rest_framework import authentication
from rest_framework import exceptions

import sys, os, urllib, re

class CASAuthentication(authentication.BaseAuthentication):
    def __init__(self):
        self.cas_url = 'https://fed.princeton.edu/cas/'

    def authenticate(self, request):

        # authentication did not succeed
        if validate(ticket) == None:
            return None
        # authentication successful
        return (user, None)

    def validate(self, ticket):
        # defines URL to be redirected to
        val_url = self.cas_url + "validate" + \
            '?service=' + urllib.quote(self.ServiceURL()) + \
            '&ticket=' + urllib.quote(ticket)
        # opens URL; should return 2 lines
        r = urllib.urlopen(val_url).readlines()
        # returns netid if there is a match
        if len(r) == 2 and re.match("yes", r[0]) != None:
            return r[1].strip()
        return None

    def serviceURL(self):
        if os.environ.has_key('REQUEST_URI'):
            ret = 'http://' + os.environ['HTTP_HOST'] + os.environ['REQUEST_URI']
            ret = re.sub(r'ticket=[^&]*&?', '', ret)
            ret = re.sub(r'\?&?$|&$', '', ret)
            return ret
        return "Something is badly wrong."
