from assets.facts.facts import random_fact
from datetime import datetime
from assets.tools.cooldown import custom_cooldown
import disnake
from disnake.ext import commands
from assets.database.log import log_command

def setup(bot : commands.Bot):
  bot.add_cog(Fact(bot))

class Fact(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot


  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  async def fact(ctx:disnake.ApplicationCommandInteraction):
    '''Ask for a fact from the awesome fact repository'''
    #calls random fact function from facts.py
    line = random_fact()
    title,desc = line[0],line[1]
    embed = disnake.Embed(title = title , description = desc, color = disnake.Color.orange(),timestamp=datetime.now())
    try:
      embed.set_image(url=line[2])
      embed.set_footer(text=line[3])
    except:
      pass
     
    if type(ctx) == disnake.channel.TextChannel:
      await ctx.send(embed=embed)
    else:
      await ctx.response.send_message(embed = embed)

    await log_command('fact',ctx.user.id)