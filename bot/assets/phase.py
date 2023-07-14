from time import strftime
from geopy import Nominatim
from requests import post
geolocator = Nominatim(user_agent = 'AstroBot')
from requests.auth import HTTPBasicAuth
from datetime import datetime
from os import environ
appid = environ['APP_ID']
secret = environ['API_KEY4']

import disnake
from disnake.ext import commands
from assets.tools.cooldown import custom_cooldown
from assets.database.log import log_command

def setup(bot : commands.Bot):
  bot.add_cog(Phase(bot))

class Phase(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  
  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
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
      embed = disnake.Embed(title = f'Moon phase at {location}', color =  disnake.Color.orange(),timestamp=datetime.now())
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

    await log_command('phase',ctx.user.id)