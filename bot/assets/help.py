import disnake
from assets.tools.cooldown import custom_cooldown
from disnake.ext import commands
from assets.database.log import log_command
from datetime import datetime

def setup(bot : commands.Bot):
  bot.add_cog(Help(bot))

class Help(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
 
 
  @commands.slash_command()
  @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  async def help(
    ctx : disnake.ApplicationCommandInteraction
  ):
    '''
    Ask for help regarding the bot's functionalities.
    '''
    await ctx.response.defer(with_message=True, ephemeral=True)
    embed = disnake.Embed(title='Help has arrived.', 
    description=
    '''
    As of now, there are only the following commands- 

    __1. `/daily`__ -  See the NASA astronomy picture of the day, along with an explanation of the picture. 
    __Specific date__  - In YYYY-MM-DD format to get an image from that date! (Example - `/daily 2005-06-08`, this was for 8th June, 2005)
    __Random APOD Photo__ - You can now request a random APOD photo from the archive using `/daily random`

    __2. `/channel`__ - get daily apod picture automatically to the channel in which you post this message. *Only for users with channel and message manage perms.*

    __3. `/remove`__- remove your channel from the daily APOD picture list. *Only for users with channel and message manage perms.*

    __4. `/info <query>`__ - The ultimate source for data, videos and pictures on ANYTHI NG related to space science.

    __5. `/iss`__ - Find the live location of the international space station with respect to the Earth.

    __6. `/fact`__ - gives a random fact from the fact library.

    __7. `/weather <location>`__ - gives the real-time weather at the specified location.

    __8. `/phase <location>`__ - To find the phase of the moon at the specified location.

    __9. `/sky <location>`__ - To get the sky map at any specified location.

    __10. `/inspace <ISS/Other>`__ - To get the information of people currently in space, in the ISS or other space stations.

    __11. `/news`__- Latest news in astronomy and space science.

    __12. `/solve`__- *NEW* use atrometry.net for solving your images.
    
    Have fun!''', color=disnake.Color.orange(),timestamp=datetime.now())
    embed.set_footer(text= "This bot has been developed with blood, tears, and loneliness by AdvaithGS#6700. Reach out for help or grievances. Vote for us at these websites")

    view = disnake.ui.View()
    topgg = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Top.gg", url="https://top.gg/bot/792458754208956466/vote")
    view.add_item(item=topgg)
    dbl = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Dbl", url="https://discordbotlist.com/bots/astrobot-2515/upvote")
    view.add_item(item=dbl)
    await ctx.followup.send(embed=embed, view=view)
    await log_command('help',ctx.user.id)

