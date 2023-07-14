from json import loads
import disnake
from disnake.ext import commands
from assets.tools.cooldown import custom_cooldown
from requests import get
from datetime import datetime
from assets.database.log import log_command
from assets.database.database import update,retrieve
db = retrieve()

def setup(bot : commands.Bot):
  bot.add_cog(Inspace(bot))

class Inspace(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot


  @commands.slash_command()  
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  async def in_space(
    ctx: disnake.ApplicationCommandInteraction,
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
    l = ['\n']
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
    embed = disnake.Embed(title = "Who's In Space" , description = s,color = disnake.Color.orange(),timestamp=datetime.now())
    if check:
      embed.set_footer(text = f"{req['iss_expedition']}th expedition of the International Space Station\nBuilt using https://github.com/corquaid/international-space-station-APIs")
      embed.set_image(url = req['expedition_image'])
    embed.add_field(name = 'Total',value = total)
    if type(ctx) == disnake.channel.TextChannel:
      await ctx.send(embed=embed)
    else:
      await ctx.response.send_message(embed = embed)

    await log_command('inspace',ctx.user.id)