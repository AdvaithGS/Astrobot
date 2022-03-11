from requests import get
from json import loads
try:
  from assets.jameswebb.image import get_image
except:
  from image import get_image
from datetime import datetime,timezone,timedelta
def get_james_webb():
  offset = timezone(timedelta(hours = 5,minutes = 30))
  now = datetime.now(offset)
  then = datetime(2021,12,25,17,30, tzinfo= timezone(timedelta(seconds=19800)))
  elapsedTime = f'{(now-then).days} days {(now-then).seconds//3600}  hours'
  data = loads(get('https://www.jwst.nasa.gov/content/webbLaunch/flightCurrentState2.0.json').text)
  data = data['currentState']
  earthkm = '`1460529.2 km`'
  l2 = '`0 km`'
  percentage = '`100 %`'
  speed = '`0.2020 km/s`'
  i = 0
  while i < len(data):
      if 'temp' not in list(data.keys())[i]:
          del data[list(data.keys())[i]]
      else:
          i += 1
  for i in data:
    data[i] = '`'+ str(data[i]) + ' °C`'
  return elapsedTime,earthkm,l2,percentage,get_image(),speed,'Webb is Orbiting L2',data