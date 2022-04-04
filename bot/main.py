#need to bring in .image and differenciate from .info,use mooncalc and suncalc
import disnake
from disnake.ext import commands
from datetime import datetime
from os import environ
from discord_components import Button
import reverse_geocoder

#from assets.database.database import *
#db = retrieve()
#
#if len(retrieve('logs')) > 200:
#  with open('log.txt','w') as f:
#    f.write(retrieve('logs'))

from assets.countries.country_code import find_country
from assets.wiki.solarsystem import get_body
from assets.wiki.wiki import get_wiki
from assets.facts.facts import random_fact
from assets.jameswebb.jameswebb import get_james_webb
from time import strftime, sleep,mktime
from requests import get,post
from requests.auth import HTTPBasicAuth
if __name__ == '__main__':
  client = commands.Bot(".", sync_commands_debug=True)
else:
  exit()
from keep_alive import keep_alive
from json import loads
from geopy import Nominatim
geolocator = Nominatim(user_agent = 'AstroBot')
import random
api_key = environ['api_key']
api_key2 = environ['api_key2']
api_key3 = environ['api_key3']
secret = environ['api_key4']
appid = environ['appid']


#generates a random activity that the bot can set as its status
async def set_activity(caller):
  pass
  #if mktime(datetime.now().timetuple()) - db['hour'] >= 21600:
  #  choice = random.choice([0,2,3,4,6,7,8,10,11,15,18])
  #  lst = ['With the stars','','The Sounds Of The Universe','Cosmos','With a bunch of Neutron stars','','.help','How The  Universe Works','Life of A Star', '', 'Richard Feynman talk about bongos','Milky Way and Andromeda collide','','','', 'The James Webb Space Telescope','','','Your .iss requests']
  #   0 - playing 1- playing and twitch  2 - Listening 3 - Watching 4 -  5- competing
  #  activity = lst[choice]
  #  choice = choice%4
  #  with open('log.txt','a') as f:
  #    time = strftime('%d/%m/%Y-%H:%M')
  #    f.write(f'\n{time} {caller}: {choice}-{activity}')
  #  with open('log.txt','r') as f:
  #    update(f.read(),'logs')
  #  db['hour'] = mktime(datetime.now().timetuple())
  #  await client.change_presence(status = disnake.Status.idle,activity = disnake.Activity(name = activity,type = choice))

async def log_command(ctx,command):
  return
  if ctx.author.id not in [756496844867108937,808262803227410465, 792458754208956466]:
    db[command] += 1

  if db['resetlast'] - mktime(datetime.now().timetuple()) >= 2592000:
    db['resetlast'] = mktime(datetime.now().timetuple())
    for i in ['daily','help','channel','remove','info','iss','fact','weather','phase','sky','webb']:
        db[i] = 0
    #update(dict(db),'db','Database reset')

  #else:
    #update(dict(db))
  
#sends APOD message if one has been released. This piece of code is triggered whenever a message in any server is sent. If it finds a new photo, it saves the updated date in db['apod'] and never does this again till the next day.
async def check_apod():
  #x = strftime('%y%m%d')
  #if db['apod'] != x and get(f'https://apod.nasa.gov/apod/ap{x}.html').status_code == 200 and loads(get(f'https://api.#nasa.gov/planetary/apod?api_key={api_key}').text) != db['daily'] and int(strftime('%H')) in range(10):
  #  db['apod'] = x
  #  req = loads(get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}').text)
  #  db['daily'] = req
  #  for guild in db.keys():
  #    try:
  #      channel = client.get_channel(db[guild])
  #      await channel.send('.daily')
  #    except:
  #      pass
  #  update(dict(db))
  pass

@client.event
async def on_ready():
  s = len(client.guilds)
  print('We have logged in as {0.user}, id {0.user.id} in {1} guilds'.format(client,s))
  # all this does is initiate the reverse_geocoder library so that .iss responses after running the server are faster
  s = (type(reverse_geocoder.search((60.12,33.12))))
  await set_activity('Startup')



@client.event
async def on_guild_join(guild):
  embed = disnake.Embed(title = 'Ooh, looks really lovely in here.', description = 'Thanks for inviting us in! I\'ll be here to help. Use `.help` to begin.', color = disnake.Color.orange())
  channel = guild.channels[0]
  for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=embed)
        break

guild_ids = [808201667543433238]
@client.slash_command(guild_ids = guild_ids)
async def daily(
  ctx,
  date : str = ''):
  '''
    Returns the Astronomy Picture Of The Day depending on the arguments given.

    Parameters
    ----------
    date: class `str` 
      It can be "random" or any date that you choose, in YYYY-MM-DD format.
  '''
  try:
    if date == '':
      daily = db['daily']
    elif date == 'random':
      delta = mktime(datetime.now().timetuple()) - mktime(datetime(1995,6,16).timetuple())
      random_date = datetime.utcfromtimestamp(mktime(datetime(1995,6,16).timetuple()) + random.randrange(int(delta)))
      parameters = {'date': f'{random_date.year}-{random_date.month}-{random_date.day}'}
      daily = loads(get (f'https://api.nasa.gov/planetary/apod?api_key={api_key}', params=parameters).text)
    else:
      parameters = {'date': date }
      daily = loads(get (f'https://api.nasa.gov/planetary/apod?api_key={api_key}', params=parameters).text)
    if 'hdurl' in daily:
      url = daily['hdurl']
      name = ''
    else:
      url = daily['url']
      name = url

    title = daily['title']
    desc = f'''{daily['date']}\nDiscover the cosmos!\n\n{daily['explanation']}\n{('Credits: '+ daily['copyright']) if 'copyright' in daily else ''}'''
    
    embed = disnake.Embed(title=title, url=url, description=desc, color=disnake.Color.orange())
    embed.set_footer(text="Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.")
    embed.set_image(url=url)
    await ctx.response.send_message(embed=embed)

    if name:
      name = f'https://youtube.com/watch?v={name[30:41]}'
      embed = disnake.Embed(title=title, url=url,   description=desc,color=disnake.Color.orange())
      await ctx.response.send_message(content = name)
    
  except Exception as e:
    print(e)
    if (get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}').text)[8:11] == '500':
      await ctx.response.send_message(content ='There\'s seems to be something wrong with the NASA APOD service, try after some time')
    else:
      await ctx.response.send_message(content ='Either your date is invalid or you\'ve chosen a date too far back. Try another one, remember, it has to be  in YYYY-MM-DD format and it also must be after 1995-06-16, the first day an APOD picture was posted')
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'daily')

@client.slash_command(guild_ids = guild_ids)
async def help(
  ctx
):
  '''
  Ask for help regarding the bot's functionalities.
  '''
  embed = disnake.Embed(title='Help has arrived.', 
  description=
  '''
  As of now, there are only the following commands- 
  
  `@AstroBot daily` or `/daily` -  See the NASA astronomy picture of the day, along with an explanation of the picture. 
  __Specific date__  - In YYYY-MM-DD format to get an image from that date! (Example - `@AstroBot daily 2005-06-08` or `/daily 2005-06-08`, this was for 8th June, 2005)
  __Random APOD Photo__ - You can now request a random APOD photo from the archive using `@AstroBot daily random` or `/daily random`
   
  `@AstroBot channel` or `/channel` - get daily apod picture automatically to the channel in which you post this message. 
   
  `@AstroBot remove` or `/remove`- remove your channel from the daily APOD picture list. 
   
  `@AstroBot info <query>` or `/info <query>` - The ultimate source for data, videos and pictures on ANYTHI NG related to space science.
  
  `@AstroBot iss` or `/iss` - Find the live location of the international space station with respect to the Earth.
  
  `@AstroBot fact` or `/fact` - gives a random fact from the fact library.
  
  `@AstroBot weather <location>` or  `/weather <location>` - gives the real-time weather at the specified location.
  
  `@AstroBot phase <location>` or `/phase <location>` - To find the phase of the moon at the specified location.
  
  `@AstroBot sky <location>` or `/sky <location>` - To get the sky map at any specified location.
  
  `@AstroBot webb` or `/webb` - To get the current state of the James Webb Space Telescope.
  
  Have fun!''', color=disnake.Color.orange())
  embed.set_footer(text= "This bot has been developed with blood, tears, and loneliness by AdvaithGS#6700 reach out to me for help or grievances. Vote for us at these websites")

  view = disnake.ui.View()
  topgg = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Top.gg", url="https://top.gg/bot/792458754208956466/vote")
  view.add_item(item=topgg)
  dbl = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Dbl", url="https://discordbotlist.com/bots/astrobot-2515/upvote")
  view.add_item(item=dbl)
  await ctx.response.send_message(embed=embed, view=view)
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'help')

@client.slash_command(guild_ids = guild_ids)
async def channel(ctx):
  '''
  Register for the automatic APOD subscription 
  '''
  if str(ctx.guild.id) not in list(db.keys()):
    db[str(ctx.guild.id)] = ctx.id
    #update(dict(db))
    embed = disnake.Embed(title = 'Registered',description = 'This channel has been registered for the Astronomy Picture of The Day service.', color=disnake.Color.orange())
    await ctx.response.send_message(embed = embed)
  else:
    embed = disnake.Embed(title = 'This server already has an APOD subscription',description = 'This channel had previously already been registered for the Astronomy Picture of The Day service.', color=disnake.Color.orange())
    await ctx.response.send_message(embed = embed)
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'channel')

@client.slash_command(guild_ids = guild_ids)
async def remove(ctx):
  '''
  Remove the channel from the APOD subscription
  '''
  if str(ctx.guild.id) in db:
    del db[str(ctx.guild.id)]
    #update(dict(db))
    embed = disnake.Embed(title = 'Unsubscribed',description = 'Removed from daily APOD feed.', color=disnake.Color.orange())
    await ctx.response.send_message(embed = embed)
  else:
    embed = disnake.Embed(title = 'Error',description = 'This server had not been registered to the APOD feed.', color=disnake.Color.orange())
    await ctx.response.send_message(embed = embed)
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'remove')

@client.slash_command(guild_ids = guild_ids)
async def info(
  ctx,
  query : str 
):
  '''
  The ultimate source for data, videos and pictures on ANYTHING related to space science.

  Parameters
  ----------
  query: class `str` 
    It can be anything pertaining to astronomy you wish to know about. 
  '''
  try:
    await ctx.response.send_message(content ='Getting the information might take some time, please wait.')
    text,image,desc = get_wiki(query)
    if text:
      embed = disnake.Embed(title = query.title() , description = text, color=disnake.Color.orange())
      get_body(embed, query)
      embed.set_footer(text = f'{desc} \n\nObtained from Solar System OpenData API and the Wikipedia API')
      embed.set_image(url = image)
    else:
      embed = disnake.Embed(title = desc , description = 'Try again with a refined search parameter', color=disnake.Color.orange())

  except:
    embed = disnake.Embed(title = 'Invalid query' , description = 'The command is `@Astrobot info <query>`. Fill a query and do not leave it blank. For example - `@Astrobot info Uranus` ,`@Astrobot info Apollo 11`', color=disnake.Color.orange())
  await ctx.edit_original_message(embed = embed)
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'info')

@client.slash_command(guild_ids = guild_ids)
async def iss(ctx):
  '''Sends the current location of the International Space Station'''
  await ctx.response.send_message('Preparing...')
  req = loads(get('https://api.wheretheiss.at/v1/satellites/25544').text)
  result = reverse_geocoder.search((round(req['latitude'],3),round(req['longitude'],3)),mode = 1)[0]
  location = ''
  if result['name']:
    location += result['name'] + ', '
  if result['admin1']:
    location += result['admin1'] + ', '
  if result['admin2']:
    location += result['admin2'] + ', '
  if result['cc']:
    location += find_country(result['cc'])
  location.replace('`', '')
  lat,long = round(req['latitude'],3),round(req['longitude'],3)
  place = f'{lat},{long}'
  url = get(f'https://www.mapquestapi.com/staticmap/v5/map?size=700,400@2x&zoom=2&defaultMarker=marker-FF0000-FFFFFF&center={place}&type=hyb&locations={place}&key={api_key2}')
  with open('iss.jpg', 'wb') as handler:
    handler.write(url.content)
  file = disnake.File('iss.jpg')
  embed = disnake.Embed(title = 'International Space Station',description = f'The International Space Station is currrently near `{location}`.' , color = disnake.Color.orange())
  embed.set_image(url = 'attachment://iss.jpg')
  velocity = round(req['velocity'],2)
  embed.add_field(name = 'Velocity' , value = f'{velocity} km/hr') 
  altitude = round(req['altitude'],2)
  embed.add_field(name = 'Altitude' , value = f'{altitude} km')
  embed.add_field(name ='Visibility',value = req['visibility'].title())
  embed.set_footer(text='This request was built using the python reverse_geocoder library, WhereTheIssAt API and the MapQuest Api.')
  await ctx.edit_original_message(embed=embed,file = file)
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'iss')


@client.slash_command(guild_ids = guild_ids)
async def fact(ctx):
  '''Ask for a fact from the awesome fact repository'''
  line = random_fact()
  title,desc = line[0],line[1]
  embed = disnake.Embed(title = title , description = desc, color = disnake.Color.orange())
  try:
    embed.set_image(url=line[2])
    embed.set_footer(text=line[3])
  except:
    pass
  await ctx.response.send_message(embed = embed)
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'fact')

@client.slash_command(guild_ids = guild_ids)
async def weather(ctx,location):
  '''
  Get the live weather for any specified location

  Parameters
  ----------
  location: class `str` 
    The place of which you want to know the weather conditions. 
  '''
  await ctx.response.send_message('Preparing...')
  try:
    req = loads(get (f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key3}&units=metric').text)
    location = location + ', ' + find_country(req['sys']['country'])
    
    result = geolocator.geocode(location)
    coords,location = result[1],result[0]
    
    embed = disnake.Embed(title = location , description = req['weather'][0]['description'].capitalize() ,color = disnake.Color.orange())
    embed.set_footer(text = 'Built using the OpenWeatherMap API and clearoutside.com')
    temp = str(req['main']['temp']) + ' °C'
    embed.add_field(name = 'Temperature', value = temp)
    lat = round(req['coord']['lat'],2)
    embed.add_field(name = 'Latitude' , value = lat)
    lon = round(req['coord']['lon'],2)
    embed.add_field(name = 'Longitude', value = lon)
    wind = str(req['wind']['speed']) + ' m/s' 
    embed.add_field(name = 'Wind Speed' , value = wind)
    sky = req['weather'][0]['main'].title()
    embed.add_field(name = 'Skies', value = sky)
    visibility = str(req['visibility']/1000) + ' km'
    embed.add_field(name = 'Visibility', value = visibility)
    
    clouds = str(req['clouds']['all']) + ' %'
    embed.add_field(name = 'Cloudiness' , value = clouds)
    for i in ['sunrise','sunset']:
      hours = int(req['timezone']/3600//1  + int(datetime.utcfromtimestamp(req['sys'][i]).strftime('%H')))
      minutes = int(req['timezone']/3600%1*60 + int(datetime.utcfromtimestamp(req['sys'][i]).strftime('%M')))
      if minutes >= 60:
        hours += 1
        minutes= minutes%60
      if hours >= 24:
        hours = hours%24
      #seconds  = int(datetime.utcfromtimestamp(req['sys'][i]).strftime('%S'))
      final_time = f'{hours}.{minutes}'
      embed.add_field(name = f'Local {i}' , value = final_time)
    icon = req['weather'][0]['icon']
    embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@2x.png")
    embed.set_image(url = f'https://clearoutside.com/forecast_image_large/{round(coords[0],2)}/{round(coords[1],2)}/forecast.png')

  except Exception as e:
    print(e)
    embed = disnake.Embed(title = 'Error' , description = 'Try again. Maybe the location is not yet in the API',color = disnake.Color.orange())
  await ctx.edit_original_message(embed = embed)
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'weather')

@client.slash_command(guild_ids = guild_ids)
async def sky(
  ctx,
  location : str
  ):
  '''
  Get the sky map for any specified location

  Parameters
  ----------
  location: class `str` 
    The place of which you want to know the sky map. 
  '''
  #Using AstronomyAPI to get .sky 
  await ctx.response.send_message('Generating....this will take some time.')
  try:
    result = geolocator.geocode(location)
    coords,location = result[1],result[0]
    if int(coords[0]) > 0:
        orientation = "north-up"
    else:
        orientation = "south-up"
    req = post("https://api.astronomyapi.com/api/v2/studio/star-chart",  auth=HTTPBasicAuth(appid, secret), 
      json = {
        "style":"default",
        "observer": {
        "latitude": coords[0],
        "longitude": coords[1],
        "date": strftime('%Y-%m-%d')
            },
        "view": {
          "type": "area",
          "parameters": {
              "position": {
                  "equatorial": {
                    "rightAscension": 1,
                    "declination": coords[0]
                  }
              },
            "zoom": 2 
            }
          }
        }
      )
    req = req.json()
    embed = disnake.Embed(title = f'Sky Map at {location}', color =   disnake.Color.orange())
    embed.add_field(name = 'Latitude',value =   f'`{round(coords[0],2)}`')
    embed.add_field(name = 'Longitude',   value = f'`{round(coords[1],2)}`')
    embed.add_field(name = 'Hemisphere',value = orientation.split('-')[0] .capitalize())
    embed.set_image(url = req['data'] ['imageUrl'])
    embed.set_footer(text = 'Generated using AstronomyAPI and python geopy  library')
  except:
    embed = disnake.Embed(title = 'Error' , description = 'Try again. Maybe the location is not yet in the API',color = disnake.Color.orange())
  await ctx.edit_original_message(embed = embed)
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'sky')

@client.slash_command(guild_ids = guild_ids)
async def phase(
  ctx,
  location : str
):
  '''
  Get the phase of the moon for any specified location

  Parameters
  ----------
  location: class `str` 
    The place of which you want to know the phase of the moon.
  '''
  await ctx.response.send_message('Generating....this will take some time.')
  try:
    result = geolocator.geocode(location)
    coords,location = result[1],result[0]
    if int(coords[0]) > 0:
      orientation = "north-up"
      ori2 = "south-up"
    else:
      orientation = "south-up" 
      ori2 = "north-up"
    req = post("https://api.astronomyapi.com/api/v2/studio/moon-phase", auth=HTTPBasicAuth(appid, secret),
    json = {
        "format": "png",
        "style": {
            "moonStyle": "default",
            "backgroundStyle": "stars",
            "backgroundColor": "red",
            "headingColor": "white",
            "textColor": "white"
        },
        "observer": {
            "latitude": coords[0],
            "longitude": coords[1],
            "date": strftime('%Y-%m-%d')
        },
        "view": {
            "type": "landscape-simple",
            'orientation': ori2
        }
    })
    req = req.json()
    embed = disnake.Embed(title = f'Moon phase at {location}', color =  disnake.Color.orange())
    embed.add_field(name = 'Latitude',value =   f'`{round(coords[0],2)}`')
    embed.add_field(name = 'Longitude',   value = f'`{round(coords[1],2)}`')
    embed.add_field(name = 'Hemisphere',value = orientation)
    embed.set_image(url = req['data'] ['imageUrl'])
    embed.set_footer(text = 'Generated using AstronomyAPI and python geopy library')
  except:
    embed = disnake.Embed(title = 'Error' , description = 'Try again. Maybe the location is not yet in the API',color = disnake.Color.orange())
  await ctx.edit_original_message(embed = embed)
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'phase')

@client.slash_command(guild_ids = guild_ids)
async def webb(ctx):
  '''
  Get the current status of the James Webb Space Telescope
  '''
  await ctx.response.send_message('Generating....this will take some time.')
  elapsedtime,image,deployment_step,temp = get_james_webb()
  embed = disnake.Embed(title = f'The James Webb Space Telescope - {deployment_step}', description = image[0] ,color =  disnake.Color.orange())
  embed.add_field(name = 'Elapsed Time',value = elapsedtime)
  embed.set_thumbnail(url="https://webb.nasa.gov/content/webbLaunch/assets/images/extra/webbTempLocationsGradient1.4TweenAll-300px.jpg")
  embed.set_image(url=image[1])
  embed.set_footer(text = 'Built using NASA\'s Where is Webb website')
  #temperatures
  places = ['Warm','Cool']
  for i in places:
    for j in ['A1AC','B2BD']:
      embed.add_field(name = f'Temp {i} Side {j[0]} ({j[ places.index(i) + 2 ]})', value = temp[f'temp{i}Side{j[1]}C'])
  for i in ['NirCam2','NirSpec3','FgsNiriss4','Miri1','Fsm5']:
    embed.add_field(name = f'{i[:-1]} ({i[-1]})',value = temp[f'tempInst{i[:-1]}K'])
  
  await ctx.edit_original_message(embed = embed)
  await check_apod()
  await set_activity('Automatic')
  await log_command(ctx,'webb')

@client.event
async def on_message(message):
  if message.content.startswith('<@!958986707376672838>'): #to be replaced
    ctx = message.channel
    mes = message.content[23:]
    '''gets the image from nasa's api, if its just 'daily' - it gets it from the database else if its the 'daily random' command, it chooses a random viable date, and sends the message. If the date is already chosen by the user, it just makes a request from the api and shares it'''
    if mes.startswith('daily'):
      try:
        parameters = {'date': mes.split(' ')[1]}
      except:
        parameters = {}
      if mes.startswith('daily random'):
        year = random.randrange(1995,2022)
        month = random.randrange(1,13)
        if month in [1,3,5,7,8,10,12]:
          date = random.randrange(1,32)
        else:
          date = random.randrange(1,31)
        if year == 1995:
          month = random.randrange(6,13)
          if month in [7,8,10,12]:
            date = random.randrange(1,32)
          elif month == 6:
            date = random.randrage(6,31)
          else:
            date = random.randrange(1,31)
        message = f'<@!808262803227410465> daily {year}-{month}-{date}'
        await ctx.send(content = message)
      else:
        try:
          if parameters == {}:
            daily = db['daily']
          else:
            daily = loads(get (f'https://api.nasa.gov/planetary/apod?api_key={api_key}', params=parameters).text)
          try:
            url = daily['hdurl']
          except:
            url = daily['url']
            name = url
  
          title = daily['title']
          desc = f'''{daily['date']}\nDiscover the cosmos!\n\n{daily['explanation']}\n{('Credits: '+ daily['copyright']) if 'copyright' in daily else ''}'''
  
          embed = disnake.Embed(title=title, url=url, description=desc, color=disnake.Color.orange())
          embed.set_footer(text="Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.")
          embed.set_image(url=url)
  
          await ctx.send(embed=embed)
  
          try:
            if name:
              name = f'https://youtube.com/watch?v={name[30:41]}'
              embed = disnake.Embed(title=title, url=url,   description=desc,color=disnake.Color.orange(),video =   {'url':url})
              await ctx.send(content = name)
          except:
            pass
        except Exception as e:
          print(e)
          if (get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}',params=parameters).text)[8:11] == '500':
            await ctx.send(content = 'There\'s seems to be something wrong with the NASA APOD service, try after some time')
          else:
            await ctx.send(content ='Either your date is invalid or you\'ve chosen a date too far back. Try another one, remember, it has to be  in YYYY-MM-DD format and it also must be after 1995-06-16, the first day an APOD picture was posted')
  


    # ask for help and commands
    elif mes.startswith('help'):
      embed = disnake.Embed(title='Help has arrived.', description=
      '''
      As of now, there are only the following commands- 
  
      `@AstroBot daily` or `/daily` -  See the NASA astronomy picture of the day, along with an explanation of the picture. 
      __Specific date__  - In YYYY-MM-DD format to get an image from that date! (Example - `@AstroBot daily 2005-06-08` or `/daily 2005-06-08`, this was for 8th June, 2005)
      __Random APOD Photo__ - You can now request a random APOD photo from the archive using `@AstroBot daily random` or `/daily random`

      `@AstroBot channel` or `/channel` - get daily apod picture automatically to the channel in which you post this message. 

      `@AstroBot remove` or `/remove`- remove your channel from the daily APOD picture list. 

      `@AstroBot info <query>` or `/info <query>` - The ultimate source for data, videos and pictures on ANYTHING related to space science.

      `@AstroBot iss` or `/iss` - Find the live location of the international space station with respect to the Earth.

      `@AstroBot fact` or `/fact` - gives a random fact from the fact library.

      `@AstroBot weather <location>` or  `/weather <location>` - gives the real-time weather at the specified location.

      `@AstroBot phase <location>` or `/phase <location>` - To find the phase of the moon at the specified location.

      `@AstroBot sky <location>` or `/sky <location>` - To get the sky map at any specified location.

      `@AstroBot webb` or `/webb` - To get the current state of the James Webb Space Telescope.

      Have fun!''', color=disnake.Color.orange())
      embed.set_footer(text= "This bot has been developed with blood, tears, and loneliness by AdvaithGS#6700 reach out to me for help or grievances. Vote for us at these websites")
      view = disnake.ui.View()
      topgg = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Top.gg", url="https://top.gg/bot/792458754208956466/vote")
      view.add_item(item=topgg)
      dbl = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Dbl", url="https://discordbotlist.com/bots/astrobot-2515/upvote")
      view.add_item(item=dbl)
      await ctx.send(embed = embed , view = view)
  
    #just something i added to trigger the daily photo if somehow the bot doesnt do it 
    #by itself. Dont blame me if you understood the reference. eheheeheh
    elif mes.lower().startswith('execute order 66'):
      if message.author.id == 756496844867108937:# my user id
        await ctx.send(content ='Are you sure, Lord Palpatine?')
        def check(msg):
          if msg.content.lower().startswith('yes'):
            return True
        try:
          message = await client.wait_for('message', timeout=60.0, check=check)
        except:
          await ctx.send(content ='Never mind.')
        else:
          await ctx.send(content ='Yes my lord.')
          for guild in db.keys():
            try:
              channel = client.get_channel(db[guild])
              await channel.send('.daily')
            except:
              pass
            
    # adds that channel to the db so that it will be sent the '.daily' message whenever an APOD image is released
    elif mes.startswith('channel'):
      if str(message.guild.id) not in list(db.keys()):
        db[str(message.guild.id)] = ctx.id
        #update(dict(db))
        await ctx.send(content ='This channel has been registered for the Astronomy Picture of The Day service.')
      else:
        await ctx.send(content ='This server was already registered.')
  
    #removes a given channel from the apod service.
    elif mes.startswith('remove'):
      if str(message.guild.id) in db:
        del db[str(message.guild.id)]
        #update(dict(db))
        await ctx.send(content ='Removed from daily APOD feed.')
      else:
        await ctx.send(content ='This server has not been registered to the APOD feed.')
  
    #New version of .info - uses the wikipedia api and solar system open data api - should give better pictures and descriptions, im also moving parts of the code outside this file into functions in 'assets'
    elif mes.startswith( 'info'):
      try:
        query = mes.split(' ',1)[1]
        await ctx.send(content ='Getting the information might take some time, please wait.')
        text,image,desc = get_wiki(query)
        if text:
          embed = disnake.Embed(title = query.title() , description = text,   color=disnake.Color.orange())
          get_body(embed, query)
          embed.set_footer(text = f'{desc} \n\nObtained from Solar System OpenData API and the Wikipedia API')
          embed.set_image(url = image)
        else:
          embed = disnake.Embed(title = desc , description = 'Try again with a refined search   parameter',   color=disnake.Color.orange())
        await ctx.send(embed = embed)
  
      except Exception as e:
        embed = disnake.Embed(title = 'Invalid query' , description = 'The command is `.info <query>`. Fill a query and do not leave it blank. For example - `.info Uranus` ,`.info Apollo 11`',   color=disnake.Color.orange())
        await ctx.send(embed = embed) 
    
    #takes info about the location of iss from wheretheiss.at and uses mapquest to obtain a map image of that
    elif mes.startswith('whereiss') or mes.startswith('iss'):
      req = loads(get('https://api.wheretheiss.at/v1/satellites/25544').text)
      result = reverse_geocoder.search((round(req['latitude'],3),round(req['longitude'],3)),mode = 1)[0]
      
      location = ''
      if result['name']:
        location += result['name'] + ', '
      if result['admin1']:
        location += result['admin1'] + ', '
      if result['admin2']:
        location += result['admin2'] + ', '
      if result['cc']:
        location += find_country(result['cc'])
      location.replace('`', '')
      lat,long = round(req['latitude'],3),round(req['longitude'],3)
      place = f'{lat},{long}'
      url = get(f'https://www.mapquestapi.com/staticmap/v5/map?size=700,400@2x&zoom=2&defaultMarker=marker-FF0000-FFFFFF&center={place}&type=hyb&locations={place}&key={api_key2}')
      with open('iss.jpg', 'wb') as handler:
        handler.write(url.content)
      file = disnake.File('iss.jpg')
      embed = disnake.Embed(title = 'International Space Station',description = f'The International Space Station is currrently near `{location}`.' , color = disnake.Color.orange())
      embed.set_image(url = 'attachment://iss.jpg')
      velocity = round(req['velocity'],2)
      embed.add_field(name = 'Velocity' , value = f'{velocity} km/hr') 
      altitude = round(req['altitude'],2)
      embed.add_field(name = 'Altitude' , value = f'{altitude} km')
      embed.add_field(name ='Visibility',value = req['visibility'].title())
      embed.set_footer(text='This request was built using the python reverse_geocoder library, WhereTheIssAt API and the MapQuest Api.')
      await ctx.send(embed=embed,file = file)
    
    #takes a fact using random_fact() method from the facts.py file which in turn obtains it from facts.txt
    elif mes.startswith('fact'):
      line = random_fact()
      title,desc = line[0],line[1]
      embed = disnake.Embed(title = title , description = desc, color = disnake.Color.orange())
      try:
        embed.set_image(url=line[2])
        embed.set_footer(text=line[3])
      except:
        pass
      await ctx.send(embed = embed)
  
    #using the open weather service API to get weather details
    elif mes.startswith('weather'):
      try:  
        location = mes.split(' ',1)[1].title()
        req = loads(get (f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key3}&units=metric').text)
        location = location + ', ' + find_country(req['sys']['country'])
        
        result = geolocator.geocode(location)
        coords,location = result[1],result[0]
        
        embed = disnake.Embed(title = location , description = req['weather'][0]['description'].capitalize() ,color = disnake.Color.orange())
        embed.set_footer(text = 'Built using the OpenWeatherMap API and clearoutside.com')
  
        temp = str(req['main']['temp']) + ' °C'
        embed.add_field(name = 'Temperature', value = temp)
  
        lat = round(req['coord']['lat'],2)
        embed.add_field(name = 'Latitude' , value = lat)
  
        lon = round(req['coord']['lon'],2)
        embed.add_field(name = 'Longitude', value = lon)
  
        wind = str(req['wind']['speed']) + ' m/s' 
        embed.add_field(name = 'Wind Speed' , value = wind)
  
        sky = req['weather'][0]['main'].title()
        embed.add_field(name = 'Skies', value = sky)
  
        visibility = str(req['visibility']/1000) + ' km'
        embed.add_field(name = 'Visibility', value = visibility)
        
        clouds = str(req['clouds']['all']) + ' %'
        embed.add_field(name = 'Cloudiness' , value = clouds)
  
        for i in ['sunrise','sunset']:
          hours = int(req['timezone']/3600//1  + int(datetime.utcfromtimestamp(req['sys'][i]).strftime('%H')))
          minutes = int(req['timezone']/3600%1*60 + int(datetime.utcfromtimestamp(req['sys'][i]).strftime('%M')))
          if minutes >= 60:
            hours += 1
            minutes= minutes%60
          if hours >= 24:
            hours = hours%24
          #seconds  = int(datetime.utcfromtimestamp(req['sys'][i]).strftime('%S'))
          final_time = f'{hours}.{minutes}'
          embed.add_field(name = f'Local {i}' , value = final_time)
  
        icon = req['weather'][0]['icon']
        embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@2x.png")
  
        embed.set_image(url = f'https://clearoutside.com/forecast_image_large/{round(coords[0],2)}/{round(coords[1],2)}/forecast.png')
  
      except Exception as e:
        print(e)
        if mes == 'weather':
          embed = disnake.Embed(title = 'Error' , description = 'Mention the name of the place. For example , `@Astrobt weather Jaipur`  ',color = disnake.Color.orange())
        else:
          embed = disnake.Embed(title = 'Error' , description = 'Try again. Maybe the location is not yet in the API',color = disnake.Color.orange())
      await ctx.send(embed = embed)
    
    #Using AstronomyAPI to get .sky 
    elif mes.startswith('sky'):
      try:
        location = mes.split(' ',1)[1].title()
        await ctx.send('Generating....this will take some time.')
        result = geolocator.geocode(location)
        coords,location = result[1],result[0]
        if int(coords[0]) > 0:
            orientation = "north-up"
        else:
            orientation = "south-up"
        req = post("https://api.astronomyapi.com/api/v2/studio/star-chart",  auth=HTTPBasicAuth(appid, secret), 
          json = {
            "style":"default",
            "observer": {
            "latitude": coords[0],
            "longitude": coords[1],
            "date": strftime('%Y-%m-%d')
                },
            "view": {
              "type": "area",
              "parameters": {
                  "position": {
                      "equatorial": {
                        "rightAscension": 1,
                        "declination": coords[0]
                      }
                  },
                "zoom": 2 
                }
              }
            }
          )
        req = req.json()
        embed = disnake.Embed(title = f'Sky Map at {location}', color =   disnake.Color.orange())
        embed.add_field(name = 'Latitude',value =   f'`{round(coords[0],2)}`')
        embed.add_field(name = 'Longitude',   value = f'`{round(coords[1],2)}`')
        embed.add_field(name = 'Hemisphere',value = orientation.split('-')[0] .capitalize())
        embed.set_image(url = req['data'] ['imageUrl'])
        embed.set_footer(text = 'Generated using AstronomyAPI and python geopy  library')
      except:
        if mes == '.sky':
          embed = disnake.Embed(title = 'Error' , description = 'Mention the name of the place. For example , `.sky Jaipur`  ',color = disnake.Color.orange())
        else:
          embed = disnake.Embed(title = 'Error' , description = 'Try again. Maybe the location is not yet in the API',color = disnake.Color.orange())
      await ctx.send(embed = embed)
    
    #Using AstronomyAPI to get .phase
    elif mes.startswith('phase'):
      try:
        location = mes.split(' ',1)[1].title()
        await ctx.send('Generating....this will take some time.')
        result = geolocator.geocode(location)
        coords,location = result[1],result[0]
        if int(coords[0]) > 0:
          orientation = "north-up"
          ori2 = "south-up"
        else:
          orientation = "south-up" 
          ori2 = "north-up"
        req = post("https://api.astronomyapi.com/api/v2/studio/moon-phase", auth=HTTPBasicAuth(appid, secret),
        json = {
            "format": "png",
            "style": {
                "moonStyle": "default",
                "backgroundStyle": "stars",
                "backgroundColor": "red",
                "headingColor": "white",
                "textColor": "white"
            },
            "observer": {
                "latitude": coords[0],
                "longitude": coords[1],
                "date": strftime('%Y-%m-%d')
            },
            "view": {
                "type": "landscape-simple",
                'orientation': ori2
            }
        })
        req = req.json()
        embed = disnake.Embed(title = f'Moon phase at {location}', color =  disnake.Color.orange())
        embed.add_field(name = 'Latitude',value =   f'`{round(coords[0],2)}`')
        embed.add_field(name = 'Longitude',   value = f'`{round(coords[1],2)}`')
        embed.add_field(name = 'Hemisphere',value = orientation)
        embed.set_image(url = req['data'] ['imageUrl'])
        embed.set_footer(text = 'Generated using AstronomyAPI and python geopy library')
      except:
        if mes == '.phase':
          embed = disnake.Embed(title = 'Error' , description = 'Mention the name of the place. For example , `.phase Jaipur`  ',color = disnake.Color.orange())
        else:
          embed = disnake.Embed(title = 'Error' , description = 'Try again. Maybe the location is not yet in the API',color = disnake.Color.orange())
      await ctx.send(embed = embed)
    
    #Taking all the data from the NASA 'WhereIsWebb?' website and from the webb tracker api
    elif mes.startswith('webb') or mes.startswith('james webb'):
      elapsedtime,image,deployment_step,temp = get_james_webb()
      embed = disnake.Embed(title = f'The James Webb Space Telescope - {deployment_step}', description = image[0] ,color =  disnake.Color.orange())
  
      embed.add_field(name = 'Elapsed Time',value = elapsedtime)
      embed.set_thumbnail(url="https://webb.nasa.gov/content/webbLaunch/assets/images/extra/webbTempLocationsGradient1.4TweenAll-300px.jpg")
      embed.set_image(url=image[1])
      embed.set_footer(text = 'Built using NASA\'s Where is Webb website')
  
      #temperatures
      places = ['Warm','Cool']
      for i in places:
        for j in ['A1AC','B2BD']:
          embed.add_field(name = f'Temp {i} Side {j[0]} ({j[ places.index(i) + 2 ]})', value = temp[f'temp{i}Side{j[1]}C'])
      for i in ['NirCam2','NirSpec3','FgsNiriss4','Miri1','Fsm5']:
        embed.add_field(name = f'{i[:-1]} ({i[-1]})',value = temp[f'tempInst{i[:-1]}K'])
      
      await ctx.send(embed = embed)
    
  
  #keeps the number of times each command has been called overall
    try:
      if mes.split()[0] in ['daily','help','channel','remove','info','iss','fact','weather','phase','sky','webb'] :#and message.author.id not in [756496844867108937,808262803227410465, 792458754208956466]:
        await log_command(message,mes.split()[0])
    except:
      pass
      
  #this info command first checks the total number of pages by going to 
  #the 100th page (since no queries are 100 pages long, the image and 
  #video api just mentions the last valid page number) and 
  #takes the last page number from there, uses the random library to pick 
  #any page from the total pages, takes the description and image and 
  #then uses the solar system open data api to pick numerical data 
  #regarding the query, if it is an astronomical body. oof.

  #UPDATE - THIS HAS BEEN REPLACED BY THE WIKIPEDIA API - IMAGES TO BE ADDED TO A NEW '.image' COMMAND  
  ''' elif mes.startswith('info'):
    try:
      q = str(mes)[6:]
      req3 = loads(get(f'https://images-api.nasa.gov/search?q={q}&page=100').text)['collection']['links'][0]['href'][-1]
      parameters = {'page': str(random.randrange(1,int(req3)+1))}
      req2 = loads(get(f'https://images-api.nasa.gov/search?q={q}',params = parameters) .text)
      choice = random.choice(dict(req2['collection'])['items'])
      desc = str(choice['data'][0]['description']).capitalize()
      embed = disnake.Embed(title = q.title() , description = desc.capitalize() ,   color=disnake.Color.orange())
      url = (choice['links'][0]['href']).replace(' ','%20') 
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
      embed.set_image(url = url)
      text = 'Built using the Solar system OpenData Api and the NASA video and image library.'
      embed.set_footer(text = text)
      await ctx.send(embed = embed)
    except:
      await ctx.send('You have not specified a query or your query is wrong, use `.info   <query>`')'''
      
  await check_apod()

  #updates the status every 6 hours - seems to not be completely working but it does change the status
  await set_activity('Automatic')

#using notepadboi as test 
client.run(environ['astrobottest'])

