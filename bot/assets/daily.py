from assets.tools.apod import apod

from assets.tools.cooldown import custom_cooldown
import disnake
from disnake.ext import commands
from assets.database.log import log_command
from os import environ
APOD_KEY = environ['APOD_KEY']

  
def setup(bot : commands.Bot):
  bot.add_cog(daily(bot))
    

class daily(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
 

  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  async def daily(
    self,
    ctx :disnake.ApplicationCommandInteraction,
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
      desc = f'''{daily['date']}\nDiscover the cosmos!\n\n{daily['desc']}\n\n{('Credits: '+ daily['credits']) if 'credits' in daily else ''}'''

      #creating an embed 
      embed = disnake.Embed(title=daily['title'], url=daily['link'], description=desc, color=disnake.Color.orange())
      embed.set_footer(text=f"Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.\nTomorrow\'s image: {daily['tomorrow']}")
      if not daily['video']:
        print("image")
        embed.set_image(url = daily['link'])
      #the message can be activated either via slash command or via message, this takes care of both instances.
      print("DAILY CALLED",daily['link']);
      await ctx.response.send_message(embed=embed)
  
      if daily['video']:
        await ctx.response.send_message(content = daily['video'])
      
    except Exception as e:
      print(e)
      
      await ctx.response.send_message(content ='Either your date is invalid or you\'ve chosen a date too far back. Try another one, remember, it has to be  in YYYY-MM-DD format and it also must be after 1995-06-16, the first day an APOD picture was posted')
    
    await log_command('daily_apod',ctx.user.id)
