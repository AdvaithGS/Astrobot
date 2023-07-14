from assets.database.database import retrieve,update
async def log_command(command,id : int ):
  if id == 756496844867108937:
    return
  db = retrieve('db')
  db[command] = db.get(command,0) + 1
  update(db,'db')
