from datetime import datetime
from time import mktime
async def log_command(command,db,update):
  try: 
    db[command] += 1
    if db['resetlast'] - mktime(datetime.now().timetuple()) >= 2592000:
      db['resetlast'] = mktime(datetime.now().timetuple())
      for i in ['daily','help','channel','remove','info','iss','fact','weather','phase','sky','webb']:
          db[i] = 0
      update(dict(db),'db','Database reset')

    else:
      update(dict(db))
  except Exception as e:
    print(e,command,'from log command')