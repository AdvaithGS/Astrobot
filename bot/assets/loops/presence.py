import disnake
from disnake.ext import tasks
from time import strftime
from itertools import cycle
from assets.database.database import update

activities = iter(cycle([[0, 'With the stars'], [2, 'The Sounds Of The Universe'],[3, 'Cosmos'], [0, 'With a bunch of Neutron stars'], [2, '/help'],[3, 'How The Universe Works'],[0, 'Life of A Star'],[2, 'Richard Feynman talk about bongos'], [3, 'Milky Way and Andromeda collide'], [3,'The James Webb Space Telescope'], [2, 'Your .iss requests' ]]))

@tasks.loop(hours = 6)
async def set_activity(client,caller):
  global activities

  activity = next(activities)
  #0 - playing 1- playing and twitch  2 - Listening 3 - Watching 4 -  5- competing

  with open('log.txt','a') as f:
    f.write(f'\n{strftime("%d/%m/%Y-%H:%M")} {caller}: {activity[0]}-{activity[1]}')
  with open('log.txt','r') as f:
    update(f.read(),'logs')
  await client.change_presence(status = disnake.Status.idle,activity = disnake.Activity(name = activity[1],type = activity[0]))

def call_set_activity(client,caller = "Automatic"):
    if not set_activity.is_running():
        set_activity.start(client,caller)