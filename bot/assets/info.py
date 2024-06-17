import disnake
from disnake.ext import commands
from assets.tools.cooldown import custom_cooldown
from assets.database.log import log_command
from assets.wiki.solarsystem import get_body
from assets.wiki.wiki import get_wiki
from datetime import datetime

def setup(bot : commands.Bot):
  bot.add_cog(Info(bot))

class Info(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
 

  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  async def info(
    ctx : disnake.ApplicationCommandInteraction,
    query : str 
  ):
    '''
    The ultimate source for data, videos and pictures on ANYTHING related to space science.
  
    Parameters
    ----------
    query: class `str` 
      It can be anything pertaining to astronomy you wish to know about. 
    '''
    await ctx.send('Generating....this will take some time.\r')
    try:
      #this get_wiki refernces get_wiki from wiki.py
      title,text,article_url,image_url = get_wiki(query)
      if text:  # create embed
        embed = disnake.Embed(title = title ,url = article_url, description = text, color=disnake.Color.orange(),timestamp=datetime.now())
        get_body(embed, query)
        embed.set_footer(text = f'Obtained from Solar System OpenData API and the Wikipedia API')
        embed.set_image(url = image_url)
      else:
        embed = disnake.Embed(title = title , description = 'Try again with a refined search parameter', color=disnake.Color.orange(),timestamp=datetime.now())
  
  #handling errors, if the query is wrong or not related to space
    except:
      embed = disnake.Embed(title = 'Invalid query' , description = 'The command is `@Astrobot info <query>`. Fill a query and do not leave it blank. For example - `@Astrobot info Uranus` ,`@Astrobot info Apollo 11`', color=disnake.Color.orange(),timestamp=datetime.now())


    await ctx.edit_original_message(embed = embed)
    await log_command('info',ctx.user.id)