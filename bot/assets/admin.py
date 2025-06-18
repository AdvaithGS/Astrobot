import disnake
from disnake.ext import commands
from assets.tools.apod import apod
from requests import get
from assets.database.database import retrieve,update
from time import strftime
from datetime import datetime

def setup(bot : commands.Bot):
  bot.add_cog(Admin(bot))

class Admin(commands.Cog):
  """This will be for a ping command."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  def check_if_it_is_me(ctx):
    return ctx.author.id == 756496844867108937

  @commands.slash_command(guild_ids = [808201667543433238])
  @commands.check(check_if_it_is_me)
  async def hello(
    self,
    ctx : disnake.ApplicationCommandInteraction):
    await ctx.response.send_message('Hello Advaith, I know you!')
  
  @commands.slash_command(guild_ids = [808201667543433238])
  @commands.check(check_if_it_is_me)
  async def execute_order_66(
    self,
    ctx: disnake.ApplicationCommandInteraction
    ):
    db_daily:dict = retrieve('daily') 
    db_guilds:dict = retrieve('guilds')
    
    await ctx.response.defer(with_message = True)

    #These are all the checks required - to check if all guilds have the latest apod and then if not, whether the apod it has is the latest 
    if all([ db_guilds[i][1]== strftime('%Y %B %d') for i in db_guilds]):
      # all good
      await ctx.response.send_message("All guilds in order")
      return
    elif db_daily['date'] != strftime('%Y %B %d'):
      x = apod()
      if x != db_daily:
        update(x,'daily')
        db_daily = x
    
    
    title = db_daily['title']
    desc = f'''{db_daily['date']}\nDiscover the cosmos!\n\n{db_daily['desc']}\n\n{('Credits: '+ db_daily['credits']) if 'credits' in db_daily else ''}'''
    embed = disnake.Embed(title=title, url=db_daily['link'], description=desc, color=disnake.Color.orange(),timestamp=datetime.now())
    embed.set_footer(text=f"Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.\nTomorrow\'s image: {db_daily['tomorrow']}")
    if not db_daily['video']:
      with open("today.jpg",'wb') as f:
        f.write(get(db_daily['link']).content)
      
      file = disnake.File("./today.jpg", filename="today.jpg")
      embed.set_image(file=file)

    apod_suc,apod_fail= 0,0
    tracker = {}
    for guild in db_guilds.keys():
      await ctx.followup.send(f"{len(db_guilds)} guilds in total..")
      if db_guilds[guild][1] != db_daily['date']: #check if they all have latest apod
        try:
          chan = self.bot.get_channel(db_guilds[guild][0])
          await chan.send(embed=embed)
          if db_daily['video']:
              await chan.send(content = db_daily['link'])
          db_guilds[guild][1] = db_daily['date'] #says they have the latest apod
          apod_suc += 1
        except Exception as e:
          if guild == 808201667543433238 and db_guilds[guild][1] != 'Sent message':
            owner = await self.bot.getch_user(self.bot.get_guild(guild).owner_id)
            embed = disnake.Embed(title= 'Daily Astronomy Picture of The Day Error',description= f'''Hello there! It seems that there has been an issue with your server "_{self.bot.get_guild(guild).name}_". The Astronomy Picture of the Day system is not correctly functioning, making the bot unable to send pictures everyday. You are requested to type the command `/channel` again and make sure Astrobot has the proper permissions (embeds,messages, etc.).\nThank you!''' , color=disnake.Color.orange(),timestamp=datetime.now())
            await owner.send(embed = embed)  
            db_guilds[guild][1] = 'Sent message'
            apod_fail += 1
    
    tracker[guild] = db_guilds[guild][1]
    embed = disnake.Embed(title = "APOD Check", description = f"Total of {len(db_guilds)} guids", color=disnake.Color.orange(),timestamp=datetime.now())
    
    for x in tracker:
      embed.add_field(name = x,value=tracker[x])
    await ctx.response.send_message(embed=embed)

    update(db_guilds,'guilds')
  # @commands.slash_command()
  # @commands.dynamic_cooldown(custom_cooldown,commands.BucketType.user)
  # async def hello(
  #   self,
  #   ctx : disnake.ApplicationCommandInteraction,
  #   query : str 
  # ):
  #   '''
  #   The ultimate source for data, videos and pictures on ANYTHING related to space science.
  
  #   Parameters
  #   ----------
  #   query: class `str` 
  #     It can be anything pertaining to astronomy you wish to know about. 
  #   '''
  #   await ctx.response.defer(with_message = True)
  #   try:
  #     #this get_wiki refernces get_wiki from wiki.py
  #     title,text,article_url,image_url = get_wiki(query)
  #     if text:  # create embed
  #       embed = disnake.Embed(title = title ,url = article_url, description = text, color=disnake.Color.orange(),timestamp=datetime.now())
  #       get_body(embed, query)
  #       embed.set_footer(text = f'Obtained from Solar System OpenData API and the Wikipedia API')
  #       embed.set_image(url = image_url)
  #     else:
  #       embed = disnake.Embed(title = title , description = 'Try again with a refined search parameter', color=disnake.Color.orange(),timestamp=datetime.now())
  
  # #handling errors, if the query is wrong or not related to space
  #   except:
  #     embed = disnake.Embed(title = 'Invalid query' , description = 'The command is `@Astrobot info <query>`. Fill a query and do not leave it blank. For example - `@Astrobot info Uranus` ,`@Astrobot info Apollo 11`', color=disnake.Color.orange(),timestamp=datetime.now())


  #   await ctx.followup.send(embed = embed)
  #   await log_command('info',ctx.user.id)


