import base64
import hashlib
import hmac
import os
import requests
import sys



def make_auth_token(upc_code, auth_key):
    sha_hash = hmac.new(auth_key.encode(), upc_code.encode(), hashlib.sha1)
    return base64.b64encode(sha_hash.digest())

def get_upc(upc_code, app_key, auth_key): 
    params = {
        'upcCode': upc_code,
        'field_names': 'all',
        'language': 'en',
        'app_key': app_key,
        'signature': make_auth_token(upc_code, auth_key)
    }
    return requests.get("https://www.digit-eyes.com/gtin/v2_0/", params).json()

if __name__ == "__main__":
    upc = get_upc(sys.argv[1], os.environ['app_key'], os.environ['auth_key'])
    print(upc)
    #print(upc['gcp']['company'])