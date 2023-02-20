import disnake
async def log_command(command,db : dict,update,ctx : disnake.User):
  if ctx.user.id == 756496844867108937:
    return
  try: 
    db[command] = db.get(command,0) + 1
    update(dict(db))
  except Exception as e:
    print(e,command,'from log command')
