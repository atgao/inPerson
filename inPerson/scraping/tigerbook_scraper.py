"""
Scraping routine for undergrads from Tigerbook.
by Alice Gao '21
"""
import hashlib
import random
from base64 import b64encode
from datetime import datetime

import requests

url = 'https://tigerbook.herokuapp.com/api/v1/undergraduates'
created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=') for i in range(32)])
username = 'atgao'
password = 'a62ac77e72fc7a1b2aec12e4dfd07367'    # use your own from /getkey
generated_digest = b64encode(hashlib.sha256((nonce + created + password).encode('utf-8')).digest())
headers = {
    'Authorization': 'WSSE profile="UsernameToken"',
    'X-WSSE': 'UsernameToken Username="%s", PasswordDigest="%s", Nonce="%s", Created="%s"' % (username, generated_digest, b64encode(nonce.encode()), created)
}

data = requests.get(url, headers=headers)
print(data.content)
