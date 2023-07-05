from requests import get
from random import random,choice
def reverse_geocode(lat : float,lon : float):
 lat,lon = round(lat,3),round(lon,3)
 req = get(f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}&zoom=10&accept-language=en').json()
 var = 2
 while req == {'error': 'Unable to geocode'}:
  var += 1
  req = get(f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat + choice([-var,+var])*random()}&lon={lon + choice([-var,+var])*random()}&zoom=10&accept-language=en').json()
 print(req['lat'],req['lon'])
 return req['display_name']

