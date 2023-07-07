from datetime import datetime
from time import mktime
from disnake.ext import tasks
# this basically logs the number of guilds astrobot has been in in various points in time. 
@tasks.loop(hours = 24)
async def stats_loop(client,stats,update):
  guilds = client.guilds
  now = mktime(datetime.now().timetuple())
  stats['member_guilds'].append([now,len(guilds)])
  update(stats,'stats')

def call_stats(client,stats,update):
    if not stats_loop.is_running():
        stats_loop.start(client,stats,update)