from assets.tools.apod import apod

import datetime
from assets.tools.cooldown import custom_cooldown
import disnake
from os import listdir, getcwd
from disnake.ext import commands
from requests import get
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
    # await ctx.response.defer(with_message = True)
    try:
      daily = apod(date)
      if not daily:
        daily.append('this is meant to break')
      desc = f'''{daily['date']}\nDiscover the cosmos!\n\n{daily['desc']}\n\n{('Credits: '+ daily['credits']) if 'credits' in daily else ''}'''

      #creating an embed 
      embed = disnake.Embed(title=daily['title'], url=daily['link'], description=desc, color=disnake.Color.orange(),timestamp = datetime.datetime.now())
    
      if not daily['video']:
        if(date == ''):
          with open("apod.jpg",'wb') as f:
            f.write(get(daily['link']).content)
            file = disnake.File("./apod.jpg", filename="apod.jpg")
        else:
          if("today.jpg" in listdir()):
            file = disnake.File("./today.jpg", filename = "today.jpg")
          else:
            print(getcwd())
            with open("apod.jpg",'wb') as f:
              f.write(get(daily['link']).content)
              file = disnake.File("./apod.jpg", filename="apod.jpg")
          
        embed.set_image(file=file)

      #the message can be activated either via slash command or via message, this takes care of both instances.
      print("DAILY CALLED",daily['link']);
      
      embed.set_footer(text=f"Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.\nTomorrow\'s image: {daily['tomorrow']}")
      
      print(daily)
      await ctx.response.send_message(embed=embed)

      if daily['video']:
        await ctx.response.send_message(content = daily['video'])
      
    except Exception as e:
      print(e)
      
      await ctx.response.send_message(content ='Either your date is invalid or you\'ve chosen a date too far back. Try another one, remember, it has to be  in YYYY-MM-DD format and it also must be after 1995-06-16, the first day an APOD picture was posted')
    
    await log_command('daily_apod',ctx.user.id)
