from requests import get
from ast import literal_eval
from assets.image import get_image
req = literal_eval(get('https://api.jwst-hub.com/track').text)
def get_james_webb():
  req = literal_eval(get('https://api.jwst-hub.com/track').text)
  req['distanceEarthKm']
  return req["launchElapsedTime"],req["distanceEarthKm"],req["distanceL2Km"],req["percentageCompleted"],get_image(),req["speedKmS"],req["currentDeploymentStep"],req['tempC']
  #distance between Earth and l2 -1446320  
#{["distanceEarthKm"]:1452394.4,"launchElapsedTime":"29:19:42:02","distanceL2Km":8134.8,"percentageCompleted":99.4427,"speedKmS":0.2033,"deploymentImgURL":"https://webb.nasa.gov/content/webbLaunch/assets/images/deployment/1000pxWide/125.png","currentDeploymentStep":"Mirror Segment Deployments COMPLETED - undefined","tempC":{"tempWarmSide1C":55,"tempWarmSide2C":12,"tempCoolSide1C":-210,"tempCoolSide2C":-202},"timestamp":"2022-01-24T08:02:02.898Z"}