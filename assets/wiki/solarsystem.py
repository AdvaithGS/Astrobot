
from requests import get
from json import loads

def get_body(embed,q):
        try:
          req = loads(get(f'https://api.le-systeme-solaire.net/rest/bodies/{q}').text)
  
          if req['mass']:
            a = str(req['mass']['massValue'])
            b = str(req['mass']['massExponent'])
            embed.add_field(name = 'Mass' , value = f'{a} x 10^{b} kg')
          else:
            embed.add_field(name = 'Mass', value = 'Unknown')
  
          if not req['density']:
            embed.add_field(name='Density' , value = 'Unknown')
          else:
            embed.add_field(name='Density' , value = str(req['density'])+ ' g/cm³')
  
          if not req['gravity']:
            embed.add_field(name='Gravity' , value = 'Unknown')
          else:
            embed.add_field(name='Gravity' , value = str(req['gravity']) + ' m/s²')
  
          if not req['sideralOrbit']:
            embed.add_field(name = 'Period of Revolution', value = 'Unknown')
          else:
            embed.add_field(name = 'Period of Revolution', value = str(req['sideralOrbit']) + '  days')
  
          if not req['sideralRotation']:
           embed.add_field(name = 'Period of Rotation', value = 'Unknown')
          else:
            embed.add_field(name = 'Period of Rotation', value = str(req['sideralRotation']) + '   hours')
  
          if req['meanRadius']:
            a = req['meanRadius']
            embed.add_field(name = 'Mean Radius' , value = f'{a} km')
          else:
            embed.add_field(name = 'Mean Radius' , value = 'Unknown')
  
          if not req['escape']:
            embed.add_field(name = 'Escape Velocity', value = 'Unknown')
          else:
            a = req['escape']
            embed.add_field(name = 'Escape Velocity', value = f'{a} m/s') 
  
          if not req['discoveredBy']:
            embed.add_field(name='Discovered By' , value = 'Unknown')
          else:
            embed.add_field(name='Discovered By' , value = req['discoveredBy'])
  
          if not req['discoveryDate']:
            embed.add_field(name='Discovery Date' , value = 'Unknown')
          else:
            embed.add_field(name='Discovery Date' , value = req['discoveryDate'])
  
          if not req['moons']:
            aroundPlanet = req['aroundPlanet']['planet'].title()
            embed.add_field(name = 'Around Planet',value = aroundPlanet)
          else:
            numMoons = len(req['moons'])
            embed.add_field(name = 'Moons',value = numMoons)
          
        except:
          pass