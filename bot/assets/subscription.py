import disnake
from assets.tools.cooldown import custom_cooldown
from disnake.ext import commands
from assets.database.log import log_command
from assets.database.database import update,retrieve
from datetime import datetime
from time import strftime

def setup(bot : commands.Bot):
  bot.add_cog(Subs(bot))

class Subs(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot


  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  @commands.has_permissions(manage_channels = True, manage_messages = True)
  async def channel(
    self,
    ctx:disnake.ApplicationCommandInteraction
  ):
    '''
    Register for the automatic APOD subscription 
    '''
    db_guilds = retrieve('guilds')
    if ctx.guild.id in db_guilds and ctx.channel.id in db_guilds[ctx.guild.id]:
      embed = disnake.Embed(title = 'This server already has an APOD subscription',description = 'This channel had previously already been registered for the Astronomy Picture of The Day service.', color=disnake.Color.orange(),timestamp=datetime.now())
    else:
      db_guilds[ctx.guild.id] = [ctx.channel.id,strftime('%Y %B %d')]
      embed = disnake.Embed(title = 'Registered',description = 'This channel has been registered for the Astronomy Picture of The Day service.', color=disnake.Color.orange(),timestamp=datetime.now())

    await ctx.response.send_message(embed=embed)
    update(db_guilds,'guilds')
    await log_command('channel',ctx.user.id)

  @commands.slash_command()
  @commands.cooldown(1, 10, type=commands.BucketType.user)
  @commands.has_permissions(manage_channels = True, manage_messages = True)
  async def remove(ctx):
    '''
    Remove the channel from the APOD subscription
    '''
    db_guilds = retrieve('guilds') 
    if ctx.guild.id in db_guilds:
      del db_guilds[ctx.guild.id]
      embed = disnake.Embed(title = 'Unsubscribed',description = 'Removed from daily APOD feed.', color=disnake.Color.orange())
    else:
      embed = disnake.Embed(title = 'Error',description = 'This server had not been registered to the APOD feed.', color=disnake.Color.orange())
    await ctx.response.send_message(embed=embed)
    update(db_guilds,'guilds')
    await log_command('remove',ctx.user.id)
  