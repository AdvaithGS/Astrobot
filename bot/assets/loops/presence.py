import disnake
from disnake.ext import tasks
from time import strftime,mktime
from datetime import datetime
from itertools import cycle

activities = iter(cycle([[0, 'With the stars'], [2, 'The Sounds Of The Universe'],[3, 'Cosmos'], [0, 'With a bunch of Neutron stars'], [2, '.help'],[3, 'How The Universe Works'],[0, 'Life of A Star'],[2, 'Richard Feynman talk about bongos'], [3, 'Milky Way and Andromeda collide'], [3,'The James Webb Space Telescope'], [2, 'Your .iss requests' ]]))

@tasks.loop(hours = 6)
async def set_activity(client,db,caller,update):
  global activities
  
  activity = next(activities)
  #0 - playing 1- playing and twitch  2 - Listening 3 - Watching 4 -  5- competing
  choice = activity[0]
  desc = activity[1]
  with open('log.txt','a') as f:
    time = strftime('%d/%m/%Y-%H:%M')
    f.write(f'\n{time} {caller}: {choice}-{desc}')
  with open('log.txt','r') as f:
    update(f.read(),'logs')
  db['hour'] = mktime(datetime.now().timetuple())
  await client.change_presence(status = disnake.Status.idle,activity = disnake.Activity(name = 'slash commands! Type /help! Reinvite the bot if that doesnt work.',type = 2))

def call_set_activity(client,db,caller,update):
  set_activity.start(client,db,caller,update)