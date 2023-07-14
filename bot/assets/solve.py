from assets.astrometry.solving import get_sub_id
import disnake
from disnake.ext import commands
from assets.tools.cooldown import custom_cooldown
from assets.database.log import log_command
from assets.database.database import update,retrieve
from datetime import datetime


def setup(bot : commands.Bot):
  bot.add_cog(Solve(bot))

class Solve(commands.Cog):
  
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  async def solve(
    ctx : disnake.ApplicationCommandInteraction,
    image : disnake.Attachment):
    '''
    Get astronmetry.com to solve your image

    Parameters
    ----------
    Image: class `disnake.Attachment` 
      The image required to be solved 
    '''
    queue = retrieve('astrometry')

    embed = disnake.Embed(title="Your image has been submitted",description = 'You will be notified in this channel when the image is completely processed.',color=disnake.Color.orange(),timestamp = datetime.now())
    embed.set_image(url = image.url)
    await ctx.response.send_message(embed = embed)
    sub_id = get_sub_id(image.url)
    queue[sub_id] = (ctx.author.id,ctx.channel.id)
    update(queue)
    await log_command('solve',ctx.user.id)
    