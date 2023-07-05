from requests import post
from json import dumps
from os import environ

astro_key = environ['api_astro']

def get_sub_id(url):
  x = post('http://nova.astrometry.net/api/login', data = {'request-json' : dumps({'apikey':astro_key})}).json()

  req = post('http://nova.astrometry.net/api/url_upload',
     data = {
       'request-json' : 
          dumps(
            { "session": x['session'], "url": url , "scale_units": "degwidth", "scale_lower": 0.1, "scale_upper": 180.0,"downsample_factor" : 2}
              )}).json()
  return req['subid']


