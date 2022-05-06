from disnake.ext import tasks
import topgg
from os import environ


async def update_votes(client):
  dbl_token = environ['topgg']
  client.topggpy = topgg.DBLClient(client, dbl_token,autopost = True)

