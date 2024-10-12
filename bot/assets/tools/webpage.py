import aiohttp
import asyncio

async def main(page, type : str, params : dict = {}):
    async with aiohttp.ClientSession() as client:
        async with client.get(page,params=params) as resp:
          if(type == "str"):
             return await resp.text()
          elif(type == "json"):
              return await resp.json()
          elif (type == 'content'):
             return await resp.read()

def get(page : str,type : str,params : dict = {}):
  loop = asyncio.get_event_loop()
  return loop.run_until_complete(main(page,type,params))
