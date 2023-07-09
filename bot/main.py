#need to bring in .image and differenciate from .info,use mooncalc and suncalc

from datetime import datetime
import disnake
from disnake.ext import commands
from os import listdir,environ
import asyncio
from assets.loops.presence import call_set_activity
from assets.loops.top import update_guilds
from assets.loops.stats import call_stats
from assets.database.database import update,retrieve
from assets.tools.apod import apod
db = retrieve()
with open('log.txt','w') as f:
  f.write(retrieve('logs'))

stats = retrieve('stats')
from time import mktime, strftime
from requests import get
if __name__ == '__main__':
  command_sync_flags = commands.CommandSyncFlags.default()
  command_sync_flags.sync_commands_debug = True
  client = commands.InteractionBot(command_sync_flags = command_sync_flags,reload = True) 
else:
  exit()
from json import loads
from geopy import Nominatim
geolocator = Nominatim(user_agent = 'AstroBot')
import random
api_key = environ['api_key']  #required for check_apod
api_key2 = environ['api_key2']
api_key3 = environ['api_key3']
secret = environ['api_key4']
appid = environ['app_id']



@client.event
async def on_ready():
  s = len(client.guilds)
  await update_guilds(client)
  print('We have logged in as {0.user}, id {0.user.id} in {1} guilds'.format(client,s))
  call_set_activity(client,db,'Startup',update)
  call_stats(client,stats,update)


#sends APOD message if one has been released. This piece of code is triggered whenever a message in any server is sent. If it finds a new photo, it saves the updated date in db['apod'] and never does this again till the next day.
async def check_apod():
    global client
    db = retrieve()
    if mktime(datetime.now().timetuple()) - db['apod_try'] <= 1200:
        pass
    if db['daily']['date'] != strftime('%Y %B %d'):
        x = apod()
    if x == db['daily']:
        db['apod_try'] = mktime(datetime.now().timetuple())
        update(db)
        await asyncio.sleep(5)
        return
    else:    
        db['daily'] = x
        update(db)
        daily = db['daily']
        title = daily['title']
        desc = f'''{daily['date']}\nDiscover the cosmos!\n\n{daily['desc']}\n\n{('Credits: '+ daily['credits']) if 'credits' in daily else ''}'''
        embed = disnake.Embed(title=title, url=daily['link'], description=desc, color=disnake.Color.orange(),timestamp=datetime.now())
        embed.set_footer(text=f"Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.\nTomorrow\'s image: {daily['tomorrow']}")
        if not daily['video']:
            embed.set_image(url=daily['link'])
        for guild in db.keys():
            if type(guild) == int and db[guild][1] != db['daily']['date']:
                try:
                    chan = client.get_channel(db[guild][0])
                    await chan.send(embed=embed)
                    if daily['video']:
                        await chan.send(content = daily['link'])
                    db[guild][1] = db['daily']['date']
                except Exception as e:
                    if guild == 808201667543433238 and db[guild][1] != 'Sent message':
                        owner = await client.getch_user(client.get_guild(guild).owner_id)
                        embed = disnake.Embed(title= 'Daily Astronomy Picture of The Day Error',description= f'''Hello there! It seems that there has been an issue with your server "_{client.get_guild(guild).name}_". The Astronomy Picture of the Day system is not correctly functioning, making the bot unable to send pictures everyday. You are requested to type the command `/channel` again and make sure Astrobot has the proper permissions (embeds,messages, etc.).\nThank you!''' , color=disnake.Color.orange(),timestamp=datetime.now())
                        await owner.send(embed = embed)
                        db[guild][1] = 'Sent message'
                update(db)
    await asyncio.sleep(10)
      


@client.event
async def on_guild_join(guild):
  embed = disnake.Embed(title = 'Ooh, looks really lovely in here.', description = 'Thanks for inviting us in! I\'ll be here to help. Use `/help` to begin.', color = disnake.Color.orange(),timestamp=datetime.now())
  for chan in guild.text_channels:
        if chan.permissions_for(guild.me).send_messages:
            await chan.send(embed=embed)
        break

async def suggestion(chan):
  if random.randint(1,20) == 4:
    suggestions = ['Astrobot has a facts database! Try `/facts`','Astrobot has a new `inspace` feature, type /inspace to get the people currently in space!',['Astrobot has a support server! Join for any queries, problems, or suggestions', disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Join", url="https://discord.gg/ZtPU67wVa5")],'Liking the bot? Leave a review on [Top.gg](https://top.gg/bot/792458754208956466/vote) and and [dbl](https://discordbotlist.com/bots/astrobot-2515/upvote)','Astrobot has a /news feature! Try it to see the latest news in astronomy ']

    choice = random.choice(suggestions)
    if type(choice[1]) == disnake.ui.Button:
      view = disnake.ui.View()
      view.add_item(choice[1])
      await chan.send(embed = disnake.Embed(title = 'Quick Tip',description = choice[0],color= disnake.Color.orange()), view = view,timestamp=datetime.now())
    else:
      await chan.send(embed = disnake.Embed(title = 'Quick Tip', description = choice,color = disnake.Color.orange(),timestamp=datetime.now()))


async def check_job_status():
  db = retrieve()
  if mktime(datetime.now().timetuple()) - db['astro_try'] <= 15:
    return
  for i in list(db['solve_queue'].keys()):
    req2 = get(f'http://nova.astrometry.net/api/submissions/{i}').json()
    if req2['processing_finished'] != 'None':
      try:
        if req2['job_calibrations']:
         job_id = req2['jobs'][0]
         image = req2['user_images'][0]
        elif req2["jobs"][0] != None and get(f'https://nova.astrometry.net/api/jobs/{req2["jobs"][0]}').json()['status'] == 'failure':
          image = req2['user_images'][0]
          job_id = 'Failure'
        else:
            continue
      except:
       continue
      if job_id == 'Failure':
        embed = disnake.Embed(title="Unsuccessful",description = 'Your submission has failed.',color=disnake.Color.red(),timestamp=datetime.now())
        embed.add_field(name = '`Job ID`', value = req2['jobs'][0])
      else:
        desc = 'This is the result of your submission.\n## Objects\n'
        
        for j in get(f'https://nova.astrometry.net/api/jobs/{job_id}/annotations/').json()['annotations']:
          desc += f"* {j['names'][-1]}: \n\t`{round(j['pixelx'],2)},{round(j['pixely'],2)}`\n"
        
        embed = disnake.Embed(title="Platesolving successful",description = desc,color=disnake.Color.orange(),timestamp=datetime.now())
        embed.add_field(name = 'Job ID', value = f'`{req2["jobs"][0]}`')
        
        #ra,dec,radius
        data = get(f'http://nova.astrometry.net/api/jobs/{job_id}/calibration/').json()
        embed.add_field(name = 'Right Ascension',value = f'`{round(data["ra"],3)}`' )
        embed.add_field(name = 'Declination', value = f'`{round(data["dec"],3)}`' )
        embed.add_field(name = 'Radius', value = f'`{round(data["radius"],3)}`' )

        link = f'https://nova.astrometry.net/annotated_display/{job_id}'
        embed.set_image(url = link)
      embed.set_footer(text = 'Made using the Astrometry API')
      chan = client.get_channel(db['solve_queue'][i][1])
      await chan.send( f'<@{db["solve_queue"][i][0]}>')
      await chan.send(embed = embed)
      del db['solve_queue'][i]
      update(db)
      await asyncio.sleep(10)
  db['astro_try'] = mktime(datetime.now().timetuple())
  update(db)
@client.event
async def on_interaction(inter):
  await check_apod()
  await suggestion(inter.channel)

for i in listdir('./bot/assets'):
  if i.endswith('.py'):
    client.load_extension(f'assets.{i[:-3]}')

@client.event
async def on_slash_command_error(ctx, error):
  if isinstance(error,commands.CommandOnCooldown):
    embed = disnake.Embed(title = "You're on cooldown", description = f"Try after {round(error.retry_after,1)} seconds." ,color = disnake.Color.red(),timestamp=datetime.now())
    await ctx.response.send_message(embed = embed)
  else:
    print(error)

@client.event
async def on_message(message):
  if message.author.id != client.user.id:
    await check_apod()
    await check_job_status()
  
client.run(environ['TOKEN'])