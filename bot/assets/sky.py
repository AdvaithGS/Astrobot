from time import strftime
from geopy import Nominatim
from requests import post
geolocator = Nominatim(user_agent = 'AstroBot')
from requests.auth import HTTPBasicAuth
from os import environ
appid = environ['app_id']
secret = environ['api_key4']
from datetime import datetime
import disnake
from assets.tools.cooldown import custom_cooldown
from disnake.ext import commands
from assets.database.log import log_command
from assets.database.database import update,retrieve
db = retrieve()

def setup(bot : commands.Bot):
  bot.add_cog(Sky(bot))

class Sky(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  
  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
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
      embed = disnake.Embed(title = f'Sky Map at {location}', color =   disnake.Color.orange(),timestamp=datetime.now())
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