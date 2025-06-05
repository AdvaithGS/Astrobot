from disnake.ext import tasks
import topgg
from os import environ

async def update_guilds(client):
  try:
    dbl_token = environ['TOPGG']
    client.topggpy = topgg.DBLClient(client, dbl_token,autopost = True)
  except:
    pass
