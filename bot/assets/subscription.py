import disnake
from assets.tools.cooldown import custom_cooldown
from disnake.ext import commands
from assets.database.log import log_command
from assets.database.database import update,retrieve
from datetime import datetime
db = retrieve()

def setup(bot : commands.Bot):
  bot.add_cog(Subs(bot))

class Subs(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot


  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  @commands.has_permissions(manage_channels = True, manage_messages = True)
  async def channel(ctx):
    '''
    Register for the automatic APOD subscription 
    '''
    if ctx.guild.id in db and ctx.channel.id in db[ctx.guild.id]:
      embed = disnake.Embed(title = 'This server already has an APOD subscription',description = 'This channel had previously already been registered for the Astronomy Picture of The Day service.', color=disnake.Color.orange(),timestamp=datetime.now())
    else:
      db[ctx.guild.id] = [ctx.channel.id,db['apod']]
      embed = disnake.Embed(title = 'Registered',description = 'This channel has been registered for the Astronomy Picture of The Day service.', color=disnake.Color.orange(),timestamp=datetime.now())

    if type(ctx) == disnake.channel.TextChannel:
      await ctx.send(embed=embed)
    else:
      await ctx.response.send_message(embed=embed)

    await log_command('channel',db,update,ctx)

  @commands.slash_command()
  @commands.cooldown(1, 10, type=commands.BucketType.user)
  @commands.has_permissions(manage_channels = True, manage_messages = True)
  async def remove(ctx):
    '''
    Remove the channel from the APOD subscription
    '''
    if ctx.guild.id in db:
      del db[ctx.guild.id]
      embed = disnake.Embed(title = 'Unsubscribed',description = 'Removed from daily APOD feed.', color=disnake.Color.orange())
    else:
      embed = disnake.Embed(title = 'Error',description = 'This server had not been registered to the APOD feed.', color=disnake.Color.orange())
    if type(ctx) == disnake.channel.TextChannel:
      await ctx.send(embed=embed)
    else:
      await ctx.response.send_message(embed=embed)
    await log_command('remove',db,update,ctx)
  