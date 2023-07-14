#need to bring in .image and differenciate from .info,use mooncalc and suncalc

from datetime import datetime
import disnake
from disnake.ext import commands
from os import listdir,environ
from assets.loops.presence import call_set_activity
from assets.loops.top import update_guilds
from assets.loops.stats import call_stats
from assets.database.database import update,retrieve
from assets.tools.apod import apod
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
from geopy import Nominatim
geolocator = Nominatim(user_agent = 'AstroBot')
import random
API_KEY = environ['API_KEY']  #required for check_apod
API_KEY2 = environ['API_KEY2']
API_KEY3 = environ['API_KEY3']
secret = environ['API_KEY4']
appid = environ['APP_ID']



@client.event
async def on_ready():
  s = len(client.guilds)
  await update_guilds(client)
  print('We have logged in as {0.user}, id {0.user.id} in {1} guilds'.format(client,s))
  call_set_activity(client,'Startup',update)
  call_stats(client,stats,update)


#This is triggered whenever a new message/interaction is sent.
#It first checks if the last time it check was more than 20 mins ago, if true, then it continues.
#Checks first if the image that is has was published on the current day
#Then if image was of earlier than today, it asks for a new image from the apod function
#If the new image now obtained is the same as the image it already has (which was of earlier than today), this means that the new image for today has not yet
#been released and it will look for the new image after 20 mins.
#It then goes to check if all servers have recieved the apod image and if not sends it to those who are missing. 
async def check_apod():
    global client
    db_tries = retrieve('tries')

    if mktime(datetime.now().timetuple()) - db_tries['apod_try'] <= 1200:
      return
    
    db_tries['apod_try'] = mktime(datetime.now().timetuple())
    update(db_tries,'tries')

    db_daily = retrieve('daily')
    if db_daily['date'] == strftime('%Y %B %d'):
      return
    else:
      x = apod()
      if x == db_daily:
        return
      update(x,'daily')
    
    db_guilds = retrieve('guilds')
    db_daily = retrieve('daily')
    if all([ db_guilds[i][1]== db_daily['date'] for i in db_guilds]):
      return
    
    title = db_daily['title']
    desc = f'''{db_daily['date']}\nDiscover the cosmos!\n\n{db_daily['desc']}\n\n{('Credits: '+ db_daily['credits']) if 'credits' in db_daily else ''}'''
    embed = disnake.Embed(title=title, url=db_daily['link'], description=desc, color=disnake.Color.orange(),timestamp=datetime.now())
    embed.set_footer(text=f"Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.\nTomorrow\'s image: {db_daily['tomorrow']}")
    if not db_daily['video']:
      embed.set_image(url=db_daily['link'])
    for guild in db_guilds.keys():
      if db_guilds[guild][1] != db_daily['date']: #check if they all have latest apod
        try:
          chan = client.get_channel(db_guilds[guild][0])
          await chan.send(embed=embed)
          if db_daily['video']:
              await chan.send(content = db_daily['link'])
          db_guilds[guild][1] = db_daily['date'] #says they have the latest apod
        except Exception as e:
          if guild == 808201667543433238 and db_guilds[guild][1] != 'Sent message':
            owner = await client.getch_user(client.get_guild(guild).owner_id)
            embed = disnake.Embed(title= 'Daily Astronomy Picture of The Day Error',description= f'''Hello there! It seems that there has been an issue with your server "_{client.get_guild(guild).name}_". The Astronomy Picture of the Day system is not correctly functioning, making the bot unable to send pictures everyday. You are requested to type the command `/channel` again and make sure Astrobot has the proper permissions (embeds,messages, etc.).\nThank you!''' , color=disnake.Color.orange(),timestamp=datetime.now())
            await owner.send(embed = embed)
            db_guilds[guild][1] = 'Sent message'
    update(db_guilds,'guilds')
      


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
  queue = retrieve('asrometry')
  tries = retrieve('tries')
  if mktime(datetime.now().timetuple()) - tries['astro_try'] <= 20:
    return
  j = 0  
  while j < len(queue):
    #schema of queue dict
    #sub_id: (user_id,channel_id)
    req2 = get(f'http://nova.astrometry.net/api/submissions/{queue[queue.keys()[j]]}').json()
    
    if req2['processing_finished'] == 'None':
      j += 1
      continue
  
    if req2['job_calibrations']:
      job_id = req2['jobs'][0]
    elif req2["jobs"][0] != None and get(f'https://nova.astrometry.net/api/jobs/{req2["jobs"][0]}').json()['status'] == 'failure':
      job_id = 'Failure'
    else:
      j += 1
      continue
    
    chan = client.get_channel(queue[queue.keys()[j]][1])
    user = queue[queue.keys()[j]][1]
    queue.pop(queue.keys()[j])
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
    await chan.send( f'<@{user}>')
    await chan.send(embed = embed)
  update(queue,'astrometry')
  tries['astro_try'] = mktime(datetime.now().timetuple())
  update(tries,'tries')

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