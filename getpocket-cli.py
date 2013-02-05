import json
import requests
import os
import sys

_CONSUMER_KEY = '11846-125392f4b355025898d85cb7'
_CONFIG_FILE = os.path.join(sys.path[0], 'getpocket-cli.json')

headers = {'content-type': 'application/json; charset=UTF8', 'X-Accept':'application/json'}

def auth_user(consumer_key):
    payload ={'consumer_key':consumer_key, 'redirect_uri':'http://www.google.com'}
    r = requests.post('https://getpocket.com/v3/oauth/request', data=json.dumps(payload), headers=headers)

    # TODO: Check response error code
    res = r.json()

    print "Please visit this URL to authorize getpocket-cli:"
    print "https://getpocket.com/auth/authorize?request_token=%s&redirect_uri=http://google.com" % res['code']
    raw_input("press ENTER when ready")

    # authorize
    payload = {'consumer_key':consumer_key, 'code': res['code']}
    r = requests.post('https://getpocket.com/v3/oauth/authorize', headers=headers, data=json.dumps(payload))
    res2 = r.json()

    print "Authorization OK for user %s" % res2['username']


    authdata = {'code':res['code'], 'access_token':res2['access_token']}

    f = open(_CONFIG_FILE, 'w')
    f.write(json.dumps(authdata))
    f.close()
    print res['code']
    print res2['access_token']

def add_url(url):
    if not url: return

    payload = json.load(file(_CONFIG_FILE))
    payload['url'] = url[0]
    print payload
    r = requests.post('https://getpocket.com/v3/add', headers=headers, data=json.dumps(payload))

    print r.text
    print r.headers


if __name__ == '__main__':
    if not os.path.exists(_CONFIG_FILE):
        auth_user(_CONSUMER_KEY)
    else:
        add_url(sys.argv[1:])
