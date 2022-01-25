from requests import get
from json import loads
from assets.image import get_image

def get_james_webb():
  req = loads(get('https://api.jwst-hub.com/track').text)
  elapsedTime = str(req["launchElapsedTime"].split(':')[0]) + ' days ' + str(req["launchElapsedTime"].split(':')[1])  +  ' hours' 
  earthkm = str(req["distanceEarthKm"]) + ' km'
  if req["distanceL2Km"] == 'None':
    l2 = '0 km'
  else:
    l2 = str(req["distanceL2Km"]) + ' km'
  percentage = str(round(req["percentageCompleted"],2)) + ' %'
  speed = str(req["speedKmS"]) + ' km/s'
  for i in req['tempC']:
    req['tempC'][i] = str(req['tempC'][i]) + ' °C'
  return elapsedTime,earthkm,l2,percentage,get_image(),speed,req["currentDeploymentStep"],req['tempC'],req['deploymentImgURL']