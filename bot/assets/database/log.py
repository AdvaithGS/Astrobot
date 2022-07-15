from datetime import datetime
from time import mktime
async def log_command(command,db,update):
  try: 
    db[command] += 1
    update(dict(db))
  except Exception as e:
    print(e,command,'from log command')
