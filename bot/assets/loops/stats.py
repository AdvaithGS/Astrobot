from datetime import datetime
from time import mktime
from disnake.ext import tasks

@tasks.loop(hours = 24)
async def stats(client,stats,update):
  guilds = client.guilds
  now = mktime(datetime.now().timetuple())
  stats['member_guilds'].append([now,len(guilds)])
  members = set()
  for guild in guilds:
    members.update(set(guild.members))
  stats['member_count'].append([now,len(members)])
  update(stats,'stats')

def call_stats(client,stats,update):
  stats.start(client,stats,update)