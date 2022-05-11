from datetime import datetime
from time import mktime
from disnake.ext import tasks

@tasks.loop(hours = 24)
async def stats(client,db):
  guilds = client.guilds
  now = mktime(datetime.now().timetuple())
  db['member_guilds'].append([now,len(guilds)])
  members = {}
  for guild in guilds:
    members.update(set(guild.members))
  db['member_count'].append([now,len(members)])

def call_stats(client,db):
  stats.start(client,db)