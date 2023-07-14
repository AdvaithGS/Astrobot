from datetime import datetime
from json import loads
from geopy import Nominatim
geolocator = Nominatim(user_agent = 'AstroBot')
from assets.countries.country_code import find_country
from os import environ
API_KEY3 = environ['API_KEY3']

import disnake
from disnake.ext import commands
from assets.tools.cooldown import custom_cooldown
from requests import get
from assets.database.log import log_command

def setup(bot : commands.Bot):
  bot.add_cog(Weather(bot))

class Weather(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
   
  
  @commands.slash_command()  
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  
  async def weather(ctx:disnake.ApplicationCommandInteraction,location):
    '''
    Get the live weather for any specified location
  
    Parameters
    ----------
    location: class `str` 
      The place of which you want to know the weather conditions. 
    '''
    # preemptively send a message to user
    await ctx.response.send_message(content = 'Preparing...')
    try:
      location = location[:]
      #query the openweathermap api for weather data
      req = loads(get (f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY3}&units=metric').text)
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
    
    await log_command('weather',ctx.user.id)