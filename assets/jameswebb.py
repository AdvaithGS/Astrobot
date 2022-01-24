from requests import get
from ast import literal_eval
from assets.image import get_image
req = literal_eval(get('https://api.jwst-hub.com/track').text)
def get_james_webb():
  req = literal_eval(get('https://api.jwst-hub.com/track').text)
  elapsedTime = str(req["launchElapsedTime"].split(':')[0]) + ' days ' + str(req["launchElapsedTime"].split(':')[1])  +  ' hours' 
  earthkm = str(req["distanceEarthKm"]) + ' km'
  l2 = str(req["distanceL2Km"]) + ' km'
  percentage = str(round(req["percentageCompleted"],2)) + ' %'
  speed = str(req["speedKmS"]) + ' km/s'
  for i in req['tempC']:
    req['tempC'][i] = str(req['tempC'][i]) + ' °C'
  return elapsedTime,earthkm,l2,percentage,get_image(),speed,req["currentDeploymentStep"],req['tempC']