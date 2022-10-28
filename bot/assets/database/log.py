async def log_command(command,db,update):
  try: 
    db[command] = db.get(command,0) + 1
    update(dict(db))
  except Exception as e:
    print(e,command,'from log command')
