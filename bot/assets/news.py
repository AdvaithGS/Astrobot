from json import loads
import random
from datetime import datetime
import disnake
from disnake.ext import commands
from assets.tools.cooldown import custom_cooldown
from requests import get
from assets.database.log import log_command
from assets.database.database import update,retrieve
db = retrieve()

def setup(bot : commands.Bot):
  bot.add_cog(News(bot))

class News(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  
  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  async def news(
      ctx :disnake.ApplicationCommandInteraction,
      limit: int = 5):
    '''
    Get the latest space news.
    
    Parameters
    ----------
    limit: class `int` 
      The number of news articles to be fetched. Default value is 5
    '''
    desc = ''
    s = loads(get(f'https://api.spaceflightnewsapi.net/v3/articles?_limit={limit}').text)
    index = 0
    for i in s:
      index += 1
      desc += f'''\n**{index}•** __[{i['title']}]({i['url']})__
      {i['summary']}
        *~{i['newsSite']}*\n'''
    embed = disnake.Embed(title="Currently happening in the realm of space",    description=desc,color=disnake.Color.orange(),timestamp=datetime.now())
    x = random.choice(s)
    embed.set_image(url = x['imageUrl'])
    embed.set_footer(text = x['title'] + '.\nGenerated using SpaceFlightNews API')
    if type(ctx) == disnake.channel.TextChannel:
      await ctx.send(embed=embed)
    else:
      await ctx.response.send_message(embed = embed)
    await log_command('news',ctx.user.id)