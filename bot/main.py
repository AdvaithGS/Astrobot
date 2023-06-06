#need to bring in .image and differenciate from .info,use mooncalc and suncalc

import disnake
from disnake.ext import commands
from datetime import datetime
from os import environ
import reverse_geocoder
import asyncio
from assets.loops.presence import call_set_activity
from assets.database.log import log_command
from assets.loops.top import update_guilds
from assets.loops.stats import call_stats
from assets.database.database import update,retrieve
from assets.apod import apod
db = retrieve()
with open('log.txt','w') as f:
  f.write(retrieve('logs'))

stats = retrieve('stats')
from assets.countries.country_code import find_country
from assets.wiki.solarsystem import get_body
from assets.wiki.wiki import get_wiki
from assets.facts.facts import random_fact
from assets.jameswebb.jameswebb import get_james_webb
from time import strftime, mktime
from requests import get,post
from requests.auth import HTTPBasicAuth
if __name__ == '__main__':
  command_sync_flags = commands.CommandSyncFlags.default()
  command_sync_flags.sync_commands_debug = True
  client = commands.InteractionBot(command_sync_flags = command_sync_flags)
else:
  exit()
from json import loads
from geopy import Nominatim
geolocator = Nominatim(user_agent = 'AstroBot')
import random
api_key = environ['api_key']
api_key2 = environ['api_key2']
api_key3 = environ['api_key3']
secret = environ['api_key4']
appid = environ['appid']


@client.event
async def on_ready():
  s = len(client.guilds)
  await update_guilds(client)
  print('We have logged in as {0.user}, id {0.user.id} in {1} guilds'.format(client,s))
  # all this does is initiate the reverse_geocoder library so that .iss responses after running the server are faster
  s = (type(reverse_geocoder.search((60.12,33.12))))
  call_set_activity(client,db,'Startup',update)
  call_stats(client,stats,update)


#sends APOD message if one has been released. This piece of code is triggered whenever a message in any server is sent. If it finds a new photo, it saves the updated date in db['apod'] and never does this again till the next day.
async def check_apod():
  global client
  if mktime(datetime.now().timetuple()) - db['apod_error'] < 1200:
    return
  if db['daily']['date'] != strftime('%Y %B %d'):
    x = apod()
    if x == db['daily']:
      return
    db['daily'] = x
    total = 0
    for i in db:
      if type(i) == int:
        total += 1
    comp = 0
    for guild in db.keys():
      if type(guild) == int and db[guild][1] != db['daily']['date']:
        try:
          chan = client.get_channel(db[guild][0])
          db[guild][1] = db['daily']['date']
          daily = db['daily']
          title = daily['title']
          desc = f'''{daily['date']}\nDiscover the cosmos!\n\n{daily['desc']}\n{('Credits: '+ daily['credits']) if 'credits' in daily else ''}'''
          embed = disnake.Embed(title=title, url=daily['link'], description=desc, color=disnake.Color.orange())
          embed.set_footer(text="Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.")
          if not daily['video']:
            embed.set_image(url=daily['link'])
          await chan.send(embed=embed)
          if daily['video']:
            await chan.send(content = daily['link'])

        except Exception as e:
          if guild in [808201667543433238,971656673334804520] and db[guild][1] != 'Sent message':
            owner : disnake.User = client.get_user(client.get_guild(guild).owner_id)
            await owner.send(f'''Hello there! It seems that there has been an issue with your server **{client.get_guild(guild).name}**. The Astronomy Picture of the Day system is not correctly functioning. You are requested to type the command `/channel` again and make sure Astrobot has the proper permissions (embeds,messages, etc.).
            Thank you!''')
            db[guild][1] = 'Sent message'
        comp += 1
        perc = round((comp/total)*(100))
        print( 'Sending daily APOD:','[' + "-"*perc + ' '*(100-perc) + ']',f'{perc}% Done.' ,end = '\r')
    await asyncio.sleep(10)
    update(db)


@client.event
async def on_guild_join(guild):
  embed = disnake.Embed(title = 'Ooh, looks really lovely in here.', description = 'Thanks for inviting us in! I\'ll be here to help. Use `/help` to begin.', color = disnake.Color.orange())
  for chan in guild.text_channels:
    if chan.permissions_for(guild.me).send_messages:
      await chan.send(embed=embed)
      break

async def suggestion(chan):
  if random.randint(1,20) == 4:
    suggestions = ['Astrobot has a facts database! Try `/facts`','Astrobot has a new `inspace` feature, type /inspace to get the people currently in space!',['Astrobot has a support server! Join for any queries, problems, or suggestions', disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Join", url="https://discord.gg/ZtPU67wVa5")],'Liking the bot? Leave a review on [Top.gg](https://top.gg/bot/792458754208956466/vote) and and [dbl](https://discordbotlist.com/bots/astrobot-2515/upvote)','Astrobot has a /news feature! Try it to see the latest news in astronomy ']

    choice = random.choice(suggestions)
    if type(choice[1]) == disnake.ui.Button:
      view = disnake.ui.View()
      view.add_item(choice[1])
      await chan.send(embed = disnake.Embed(title = 'Quick Tip',description = choice[0],color= disnake.Color.orange()), view = view)
    else:
      await chan.send(embed = disnake.Embed(title = 'Quick Tip', description = choice,color= disnake.Color.orange()))

@client.event
async def on_interaction(inter):
  await check_apod()
  await suggestion(inter.channel)

@client.slash_command()
@commands.cooldown(1, 10, type=commands.BucketType.user)
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
    daily = apod(date)
    if not daily:
      daily.append('this is meant to break')
    desc = f'''{daily['date']}\nDiscover the cosmos!\n\n{daily['explanation']}\n{('Credits: '+ daily['credits']) if 'credits' in daily else ''}'''

    #creating an embed 
    embed = disnake.Embed(title=daily['title'], url=daily['link'], description=desc, color=disnake.Color.orange())
    embed.set_footer(text=f"Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.\nTomorrow\'s image: {daily['tomorrrow']}")
    if not daily['video']:
      embed.set_image(url = daily['link'])
    #the message can be activated either via slash command or via message, this takes care of both instances.
    if type(ctx) == disnake.channel.TextChannel:
      await ctx.send(embed=embed)
    else:
      await ctx.response.send_message(embed=embed)

    if daily['video']:
      if type(ctx) == disnake.channel.TextChannel:
        await ctx.send(daily['video'])
      else:
        await ctx.response.send_message(content = daily['video'])
    
  except Exception as e:
    if type(ctx) == disnake.channel.TextChannel:
      await ctx.send('Either your date is invalid or you\'ve chosen a date too far back. Try another one, remember, it has to be  in YYYY-MM-DD format and it also must be after 1995-06-16, the first day an APOD picture was posted')
    else:
      await ctx.response.send_message(content ='Either your date is invalid or you\'ve chosen a date too far back. Try another one, remember, it has to be  in YYYY-MM-DD format and it also must be after 1995-06-16, the first day an APOD picture was posted')
  await log_command('daily_apod',db,update,ctx)

@client.slash_command()
@commands.cooldown(1, 10, type=commands.BucketType.user)
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
  
  __1. `/daily`__ -  See the NASA astronomy picture of the day, along with an explanation of the picture. 
  __Specific date__  - In YYYY-MM-DD format to get an image from that date! (Example - `/daily 2005-06-08`, this was for 8th June, 2005)
  __Random APOD Photo__ - You can now request a random APOD photo from the archive using `/daily random`
   
  __2. `/channel`__ - get daily apod picture automatically to the channel in which you post this message. 
   
  __3. `/remove`__- remove your channel from the daily APOD picture list. 
   
  __4. `/info <query>`__ - The ultimate source for data, videos and pictures on ANYTHI NG related to space science.
  
  __5. `/iss`__ - Find the live location of the international space station with respect to the Earth.
  
  __6. `/fact`__ - gives a random fact from the fact library.
  
  __7. `/weather <location>`__ - gives the real-time weather at the specified location.
  
  __8. `/phase <location>`__ - To find the phase of the moon at the specified location.
  
  __9. `/sky <location>`__ - To get the sky map at any specified location.

  __10. `/inspace <ISS/Other>`__ - To get the information of people currently in space, in the ISS or other space stations.

  __11. `/news`__- Latest news in astronomy and space science.
  
  Have fun!''', color=disnake.Color.orange())
  embed.set_footer(text= "This bot has been developed with blood, tears, and loneliness by AdvaithGS#6700. Reach out for help or grievances. Vote for us at these websites")

  view = disnake.ui.View()
  topgg = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Top.gg", url="https://top.gg/bot/792458754208956466/vote")
  view.add_item(item=topgg)
  dbl = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Dbl", url="https://discordbotlist.com/bots/astrobot-2515/upvote")
  view.add_item(item=dbl)
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed=embed, view=view)
  else:
    await ctx.response.send_message(embed=embed, view=view)
  await log_command('help',db,update,ctx)

@client.slash_command()
@commands.cooldown(1, 10, type=commands.BucketType.user)
async def channel(ctx):
  '''
  Register for the automatic APOD subscription 
  '''
  if ctx.guild.id in db and ctx.channel.id in db[ctx.guild.id]:
    embed = disnake.Embed(title = 'This server already has an APOD subscription',description = 'This channel had previously already been registered for the Astronomy Picture of The Day service.', color=disnake.Color.orange())
  else:
    db[ctx.guild.id] = [ctx.channel.id,db['apod']]
    embed = disnake.Embed(title = 'Registered',description = 'This channel has been registered for the Astronomy Picture of The Day service.', color=disnake.Color.orange())

  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed=embed)
  else:
    await ctx.response.send_message(embed=embed)

  await log_command('channel',db,update,ctx)

@client.slash_command()
@commands.cooldown(1, 10, type=commands.BucketType.user)
async def remove(ctx):
  '''
  Remove the channel from the APOD subscription
  '''
  if ctx.guild.id in db:
    del db[ctx.guild.id]
    embed = disnake.Embed(title = 'Unsubscribed',description = 'Removed from daily APOD feed.', color=disnake.Color.orange())
  else:
    embed = disnake.Embed(title = 'Error',description = 'This server had not been registered to the APOD feed.', color=disnake.Color.orange())
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed=embed)
  else:
    await ctx.response.send_message(embed=embed)
  await log_command('remove',db,update,ctx)

@client.slash_command()
@commands.cooldown(1, 60, type=commands.BucketType.user)
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
    query = query[:]
    if type(ctx) == disnake.channel.TextChannel:
      await ctx.send('Getting the information might take some time, please wait.')
    else:
      await ctx.response.send_message(content ='Getting the information might take some time, please wait.')
    #this get_wiki refernces get_wiki from wiki.py
    title,text,article_url,image_url = get_wiki(query)
    if text:  # create embed
      embed = disnake.Embed(title = title ,url = article_url, description = text, color=disnake.Color.orange())
      get_body(embed, query)
      embed.set_footer(text = f'Obtained from Solar System OpenData API and the Wikipedia API')
      embed.set_image(url = image_url)
    else:
      embed = disnake.Embed(title = title , description = 'Try again with a refined search parameter', color=disnake.Color.orange())

#handling errors, if the query is wrong or not related to space
  except:
    embed = disnake.Embed(title = 'Invalid query' , description = 'The command is `@Astrobot info <query>`. Fill a query and do not leave it blank. For example - `@Astrobot info Uranus` ,`@Astrobot info Apollo 11`', color=disnake.Color.orange())

  
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed=embed)
  else:
    await ctx.edit_original_message(embed = embed)
  await log_command('info',db,update,ctx)

@client.slash_command()
@commands.cooldown(1, 30, type=commands.BucketType.user)
async def iss(ctx):
  '''Sends the current location of the International Space Station'''
  # sends a preemptive message to users
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send('Preparing...')
  else:
    await ctx.response.send_message(content = 'Preparing...')

  #queries wheretheissat api
  req = loads(get('https://api.wheretheiss.at/v1/satellites/25544').text)
  #parsing info from api response
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
  #gets map image
  url = get(f'https://www.mapquestapi.com/staticmap/v5/map?size=700,400@2x&zoom=2&defaultMarker=marker-FF0000-FFFFFF&center={place}&type=hyb&locations={place}&key={api_key2}')
  with open('iss.jpg', 'wb') as f:
    f.write(url.content) #saves image as file
  file = disnake.File('iss.jpg') #creates file object for attaching to embed
  embed = disnake.Embed(title = 'International Space Station',description = f'The International Space Station is currrently near `{location}`.' , color = disnake.Color.orange())
  embed.set_image(url = 'attachment://iss.jpg')
  velocity = round(req['velocity'],2)
  embed.add_field(name = 'Velocity' , value = f'{velocity} km/hr') 
  altitude = round(req['altitude'],2)
  embed.add_field(name = 'Altitude' , value = f'{altitude} km')
  embed.add_field(name ='Visibility',value = req['visibility'].title())
  embed.set_footer(text='This request was built using the python reverse_geocoder library, WhereTheIssAt API and the MapQuest Api.')

  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed=embed,file = file)
  else:
    await ctx.edit_original_message(embed = embed,file = file)

  await log_command('iss',db,update,ctx)

@client.slash_command()
@commands.cooldown(1,30,type = commands.BucketType.user)
async def news(ctx):
  '''
  Get the latest space news.
  '''
  desc = ''
  s = loads(get('https://api.spaceflightnewsapi.net/v3/articles?_limit=5').text)
  index = 0
  for i in s:
    index += 1
    desc += f'''\n**{index}•** __[{i['title']}]({i['url']})__
    {i['summary']}
      *~{i['newsSite']}*\n'''
  embed = disnake.Embed(title="Currently happening in the realm of space",    description=desc,color=disnake.Color.orange())
  x = random.choice(s)
  embed.set_image(url = x['imageUrl'])
  embed.set_footer(text = x['title'] + '.\nGenerated using SpaceFlightNews API')
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed=embed)
  else:
    await ctx.response.send_message(embed = embed)
  await log_command('news',db,update,ctx)

@client.slash_command()
@commands.cooldown(1, 10, type=commands.BucketType.user)
async def fact(ctx):
  '''Ask for a fact from the awesome fact repository'''
  #calls random fact function from facts.py
  line = random_fact()
  title,desc = line[0],line[1]
  embed = disnake.Embed(title = title , description = desc, color = disnake.Color.orange())
  try:
    embed.set_image(url=line[2])
    embed.set_footer(text=line[3])
  except:
    pass

  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed=embed)
  else:
    await ctx.response.send_message(embed = embed)

  await log_command('fact',db,update,ctx)

@client.slash_command()
@commands.cooldown(1, 30, type=commands.BucketType.user)
async def weather(ctx,location):
  '''
  Get the live weather for any specified location

  Parameters
  ----------
  location: class `str` 
    The place of which you want to know the weather conditions. 
  '''
  # preemptively send a message to user
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send('Preparing...')
  else:
    await ctx.response.send_message(content = 'Preparing...')
  try:
    location = location[:]
    #query the openweathermap api for weather data
    req = loads(get (f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key3}&units=metric').text)
    location = location + ', ' + find_country(req['sys']['country'])
    
    #use geopy for getting coordinates from user given location  
    result = geolocator.geocode(location)
    coords,location = result[1],result[0]
    
    #### parse data
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
    skies = req['weather'][0]['main'].title()
    embed.add_field(name = 'Skies', value = skies)
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
      final_time = f'{hours}.{minutes}'
      embed.add_field(name = f'Local {i}' , value = final_time)
    ####
    
    icon = req['weather'][0]['icon']
    embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@2x.png")
    embed.set_image(url = f'https://clearoutside.com/forecast_image_large/{round(coords[0],2)}/{round(coords[1],2)}/forecast.png')

  except Exception as e:
    if type(location) == str: # handling errors
      embed = disnake.Embed(title = 'Error' , description = 'Try again. Maybe the location is not yet in the API',color = disnake.Color.orange())
    else:
      embed = disnake.Embed(title = 'Invalid query' , description = 'The command is `@Astrobot weather <query>`. Fill a query and do not leave it blank. For example - `@Astrobot weather Madrid` ,`@Astrobot weather Raipur`', color=disnake.Color.orange())
  
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed = embed)
  else:
    await ctx.edit_original_message(embed = embed)
  
  await log_command('weather',db,update,ctx)

@client.slash_command()
@commands.cooldown(1,30, type=commands.BucketType.user)
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

  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send('Generating....this will take some time.')
  else:
    await ctx.response.send_message('Generating....this will take some time.')

  try:
    location = location[:]
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
    if type(location) == str:
      embed = disnake.Embed(title = 'Error' , description = 'Try again. Maybe the location is not yet in the API',color = disnake.Color.orange())
    else:
      embed = disnake.Embed(title = 'Invalid query' , description = 'The command is `@Astrobot sky <query>`. Fill a query and do not leave it blank. For example - `@Astrobot sky Laos` ,`@Astrobot sky Quito`', color=disnake.Color.orange())
  
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed = embed)
  else:
    await ctx.edit_original_message(embed = embed)
  
  await log_command('sky',db,update,ctx)

@client.slash_command()
@commands.cooldown(1, 30, type=commands.BucketType.user)
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
  #preemptively send a message to the user
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send('Generating....this will take some time.')
  else:
    await ctx.response.send_message('Generating....this will take some time.')


  try:
    location = location[:]

    #get coordinates of location given by user
    result = geolocator.geocode(location)
    coords,location = result[1],result[0]
    if int(coords[0]) > 0:
      orientation = "north-up"
      ori2 = "south-up"
    else:
      orientation = "south-up" 
      ori2 = "north-up"
    #querying astronomyapi
    req = post("https://api.astronomyapi.com/api/v2/studio/moon-phase", auth=HTTPBasicAuth(appid, secret),
    json = { # this is all the paramters that will be given to the api
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
    #picking data and putting into embed
    embed = disnake.Embed(title = f'Moon phase at {location}', color =  disnake.Color.orange())
    embed.add_field(name = 'Latitude',value =   f'`{round(coords[0],2)}`')
    embed.add_field(name = 'Longitude',   value = f'`{round(coords[1],2)}`')
    embed.add_field(name = 'Hemisphere',value = orientation)
    embed.set_image(url = req['data'] ['imageUrl'])
    embed.set_footer(text = 'Generated using AstronomyAPI and python geopy library')
  except: #hadling errors
    if type(location) == str:
      embed = disnake.Embed(title = 'Error' , description = 'Try again. Maybe the location is not yet in the API',color = disnake.Color.orange())
    else:
      embed = disnake.Embed(title = 'Invalid query' , description = 'The command is `@Astrobot phase <query>`. Fill a query and do not leave it blank. For example - `@Astrobot phase Kolkata` ,`@Astrobot phase Alsace`', color=disnake.Color.orange())
  
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed = embed)
  else:
    await ctx.edit_original_message(embed = embed)

  await log_command('phase',db,update,ctx)

@client.slash_command()
@commands.cooldown(1,30,type = commands.BucketType.user)
async def in_space(
  ctx,
  location:str= commands.Param(choices=['ISS','Other'])):
  '''
  Get the people currently in space.

  Parameters
  ----------
  location: class `str` 
    Search for people in a specific station.
  '''
  req = loads(get('https://corquaid.github.io/international-space-station-APIs/JSON/people-in-space.json').text)
  check = (location == 'ISS')
  l = ['People currently in space']
  total = 0
  for i in req['people']:
    if i['iss'] == check:
      total += 1
      l.append(
      f'''
      *{i['name']}*
      Country : {i['country']} :flag_{i['flag_code']}:
      Position : `{i['position']}`
      Agency : `{i['agency']}`
      Days in space : {i['days_in_space']}
      [Wiki]({i['url']}) |  [Image]({i['image']})   
      ''')
  s = ''.join(l)
  total = '`'+str(total)+'`'
  embed = disnake.Embed(title = "Who's In Space" , description = s,color = disnake.Color.orange())
  if check:
    embed.set_footer(text = f"{req['iss_expedition']}th expedition of the International Space Station\n Built using https://github.com/corquaid/international-space-station-APIs")
    embed.set_image(url = req['expedition_image'])
  embed.add_field(name = 'Total',value = total)
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed=embed)
  else:
    await ctx.response.send_message(embed = embed)

  await log_command('inspace',db,update,ctx)

@client.slash_command()
@commands.cooldown(1, 30, type=commands.BucketType.user)
async def webb(ctx):
  '''
  Get the current status of the James Webb Space Telescope
  '''

  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send('Generating....this will take some time.')
  else:
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
  
  
  if type(ctx) == disnake.channel.TextChannel:
    await ctx.send(embed = embed)
  else:
    await ctx.edit_original_message(embed = embed)

  await log_command('webb',db,update,ctx)

@client.event
async def on_slash_command_error(ctx, error):
  if isinstance(error,commands.CommandOnCooldown):
    embed = disnake.Embed(title = "You're on cooldown", description = f"Try after {round(error.retry_after,1)} seconds." ,color = disnake.Color.red())
    await ctx.response.send_message(embed = embed)
  else:
    print(error)

@client.event
async def on_message(message):
  if message.content.startswith('<@792458754208956466>'): #to be replaced
    ctx = message.channel
    mes = message.content[22:]
    '''gets the image from nasa's api, if its just 'daily' - it gets it from the database else if its the 'daily random' command, it chooses a random viable date, and sends the message. If the date is already chosen by the user, it just makes a request from the api and shares it'''
    if mes.startswith('daily'):
      try:
        await daily(ctx,mes.split(' ',1)[1])
      except:
        await daily(ctx,'')

    # ask for help and commands
    elif mes.startswith('help'):
      await help(ctx)
  
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
              chan = client.get_channel(db[guild])
              await chan.send('<@792458754208956466> daily')
            except:
              pass
            
    # adds that channel to the db so that it will be sent the '.daily' message whenever an APOD image is released
    elif mes.startswith('channel'):
      await channel(message)
  
    #removes a given channel from the apod service.
    elif mes.startswith('remove'):
      await remove(message)
  
    #New version of .info - uses the wikipedia api and solar system open data api - should give better pictures and descriptions, im also moving parts of the code outside this file into functions in 'assets'
    elif mes.startswith( 'info'):
      try:
        query = mes.split(' ',1)[1]
        await info(ctx,query)
      except:
        await info(ctx,None)

    
    #takes info about the location of iss from wheretheiss.at and uses mapquest to obtain a map image of that
    elif mes.startswith('whereiss') or mes.startswith('iss'):
      await iss(ctx)
    
    #takes a fact using random_fact() method from the facts.py file which in turn obtains it from facts.txt
    elif mes.startswith('fact'):
      await fact(ctx)
  
    #using the open weather service API to get weather details
    elif mes.startswith('weather'):
      try:
        location = mes.split(' ',1)[1].title()
        await weather(ctx,location)
      except:
        await weather(ctx,None)

    #Using AstronomyAPI to get .sky 
    elif mes.startswith('sky'):
      try:
        location = mes.split(' ',1)[1].title()
        await sky(ctx,location)
      except:
        await sky(ctx,None)
    
    #Using AstronomyAPI to get .phase
    elif mes.startswith('phase'):
      try:
        location = mes.split(' ',1)[1].title()
        await phase(ctx,location)
      except:
        await phase(ctx,None)
    #Taking all the data from the NASA 'WhereIsWebb?' website and from the webb tracker api
    elif mes.startswith('webb') or mes.startswith('james webb'):
      await webb(ctx)
      
    await suggestion(ctx)
  await check_apod()
client.run(environ['TOKEN'])

