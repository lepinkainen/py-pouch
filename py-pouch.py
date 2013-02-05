#!/usr/bin/env python
import json
import requests
import os
import sys

_CONSUMER_KEY = '11849-770904ff3fd15ab892c822fb'
_CONFIG_FILE = os.path.join(sys.path[0], 'py-pouch.json')
_REDIRECT_URL = 'https://github.com/lepinkainen/py-pouch/wiki/Auth-OK'

__DEBUG = False

headers = {'content-type': 'application/json; charset=UTF8', 'X-Accept':'application/json'}

def auth_user(consumer_key):
    print("No configuration file found, will now attempt to authenticate with Pocket")

    payload ={'consumer_key':consumer_key, 'redirect_uri':_REDIRECT_URL}
    r = requests.post('https://getpocket.com/v3/oauth/request', headers=headers, data=json.dumps(payload))

    if r.status_code != 200:
        print("Unexpected error while requesting user code, exiting.")
        for k,v in r.headers.items():
            print "%22s: %s" % (k,v)
        sys.exit(1)

    res = r.json()

    print("Please visit this URL to authorize py-pouch:")
    print("https://getpocket.com/auth/authorize?request_token=%s&redirect_uri=%s" % (res['code'], _REDIRECT_URL))
    raw_input("press ENTER when ready")

    # authorize
    payload = {'consumer_key':consumer_key, 'code': res['code']}
    r = requests.post('https://getpocket.com/v3/oauth/authorize', headers=headers, data=json.dumps(payload))

    if r.status_code != 200:
        print("Unexpected error during authorization, exiting.")
        for k,v in r.headers.items():
            print "%22s: %s" % (k,v)
        sys.exit(1)

    res2 = r.json()

    print("Authorization OK for user %s" % res2['username'])

    # Save authentication data to file
    authdata = {'access_token':res2['access_token']}
    f = open(_CONFIG_FILE, 'w')
    f.write(json.dumps(authdata))
    f.close()

    print("Configuration file saved")

def add_url(url):
    if not url: return

    payload = json.load(file(_CONFIG_FILE))
    payload['consumer_key'] = _CONSUMER_KEY
    payload['url'] = url[0]
    payload['tags'] = "py-pouch"
    r = requests.post('https://getpocket.com/v3/add', headers=headers, data=json.dumps(payload))

    if r.status_code != 200:
        print("Error while adding url: %s" % r.headers['x-error'])
        if __DEBUG:
            for k,v in r.headers.items():
                print "%22s: %s" % (k,v)
    else:
        if __DEBUG:
            for k,v in r.json()['item'].items():
                print "%22s: %s" % (k,v)

# Stub, modify API is different from the others
def modify_url(url, action):
    if not url: return

    payload = json.load(file(_CONFIG_FILE))
    payload['action'] = action
    payload['url'] = url[0]
    print payload
    r = requests.post('https://getpocket.com/v3/modify', headers=headers, data=json.dumps(payload))

    if r.status_code != 200:
        print("Error while modifying url:")
        for k,v in r.headers.items():
            print "%22s: %s" % (k,v)

if __name__ == '__main__':
    # Check for existing auth, if none exists, authenticate
    if not os.path.exists(_CONFIG_FILE):
        auth_user(_CONSUMER_KEY)

    # Auth exists, attempt to add url
    if os.path.exists(_CONFIG_FILE):
        add_url(sys.argv[1:])
