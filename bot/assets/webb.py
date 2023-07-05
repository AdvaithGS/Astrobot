from assets.jameswebb.jameswebb import get_james_webb

import disnake
from disnake.ext import commands
from assets.database.log import log_command
from assets.database.database import update,retrieve
from datetime import datetime
from assets.tools.cooldown import custom_cooldown
db = retrieve()

def setup(bot : commands.Bot):
  bot.add_cog(Webb(bot))

class Webb(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot


  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  async def webb(ctx):
    '''
    Get the current status of the James Webb Space Telescope
    '''

    if type(ctx) == disnake.channel.TextChannel:
      await ctx.send('Generating....this will take some time.')
    else:
      await ctx.response.send_message('Generating....this will take some time.')

    elapsedtime,image,deployment_step,temp = get_james_webb()
    embed = disnake.Embed(title = f'The James Webb Space Telescope - {deployment_step}', description = image[0] ,color =  disnake.Color.orange(),timestamp = datetime.now())
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