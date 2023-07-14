from json import loads
from requests import get
from os import environ
from datetime import datetime
import disnake
from assets.tools.cooldown import custom_cooldown
from disnake.ext import commands
from assets.database.log import log_command
from assets.countries.reverse import reverse_geocode

API_KEY2 = environ['API_KEY2']

def setup(bot : commands.Bot):
  bot.add_cog(ISS(bot))

class ISS(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot


  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  async def iss(ctx:disnake.ApplicationCommandInteraction):
    '''Gets the current location of the International Space Station'''
    # sends a preemptive message to users
    if type(ctx) == disnake.channel.TextChannel:
      await ctx.send('Preparing...')
    else:
      await ctx.response.send_message(content = 'Preparing...')

    #queries wheretheissat api
    req = loads(get('https://api.wheretheiss.at/v1/satellites/25544').text)
    location = reverse_geocode(req['latitude'],req['longitude'])
    lat,long = round(req['latitude'],3),round(req['longitude'],3)
    place = f'{lat},{long}'
    #gets map image
    url = get(f'https://www.mapquestapi.com/staticmap/v5/map?size=700,400@2x&zoom=2&defaultMarker=marker-FF0000-FFFFFF&center={place}&type=hyb&locations={place}&key={API_KEY2}')
    with open('iss.jpg', 'wb') as f:
      f.write(url.content) #saves image as file
    file = disnake.File('iss.jpg') #creates file object for attaching to embed
    embed = disnake.Embed(title = 'International Space Station',description = f'The International Space Station is currrently near `{location}`.' , color = disnake.Color.orange(),timestamp=datetime.now())
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

    await log_command('iss',ctx.user.id)