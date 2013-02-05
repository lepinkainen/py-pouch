#!/usr/bin/env python
import json
import requests
import os
import sys

_CONSUMER_KEY = '11849-770904ff3fd15ab892c822fb'
_CONFIG_FILE = os.path.join(sys.path[0], 'py-pouch.json')
_REDIRECT_URL = 'https://github.com/lepinkainen/py-pouch/wiki/Auth-OK'

headers = {'content-type': 'application/json; charset=UTF8', 'X-Accept':'application/json'}

def auth_user(consumer_key):
    print("No configuration file found, will now attempt to authenticate with getpocket")

    payload ={'consumer_key':consumer_key, 'redirect_uri':'http://www.google.com'}
    r = requests.post('https://getpocket.com/v3/oauth/request', data=json.dumps(payload), headers=headers)

    if r.status_code != 200:
        print("Unexpected error while requesting user code, exiting.")
        sys.exit(1)

    res = r.json()

    print("Please visit this URL to authorize getpocket-cli:")
    print("https://getpocket.com/auth/authorize?request_token=%s&redirect_uri=%s" % (res['code'], _REDIRECT_URL))
    raw_input("press ENTER when ready")

    # authorize
    payload = {'consumer_key':consumer_key, 'code': res['code']}
    r = requests.post('https://getpocket.com/v3/oauth/authorize', headers=headers, data=json.dumps(payload))
    if r.status_code != 200:
        print("Unexpected error during authorization, exiting.")
        sys.exit(1)

    res2 = r.json()

    print("Authorization OK for user %s" % res2['username'])

    # Save authentication data to file
    authdata = {'code':res['code'], 'access_token':res2['access_token']}
    f = open(_CONFIG_FILE, 'w')
    f.write(json.dumps(authdata))
    f.close()

    print("Configuration file saved")

def add_url(url):
    if not url: return

    payload = json.load(file(_CONFIG_FILE))
    payload['url'] = url[0]
    r = requests.post('https://getpocket.com/v3/add', headers=headers, data=json.dumps(payload))

    if r.status_code != 200:
        print("Error while adding url:")
        for k,v in r.headers.items():
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
        print("Error while adding url:")
        for k,v in r.headers.items():
            print "%22s: %s" % (k,v)

if __name__ == '__main__':
    if not os.path.exists(_CONFIG_FILE):
        auth_user(_CONSUMER_KEY)

    if os.path.exists(_CONFIG_FILE):
        add_url(sys.argv[1:])
