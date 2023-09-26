from os import environ
from github import Github
from github import Auth 
auth = Auth.Token(environ['API_KEY6'])
github = Github(auth = auth)
from time import strftime
repository = github.get_user().get_repo('db')

def contents(filename):
  return repository.get_contents(filename)

def update(db,filename,remarks = f"update file on {strftime('%H:%M %d/%m/%Y')}"):
  contents = contents(filename)
  content = str(db)
  f = repository.update_file(filename, remarks, content, contents.sha)
  
def retrieve(filename:str) -> dict:
  """Returns the dictionary contained in the mentioned filename."""
  try:
    db = eval(contents(filename).decoded_content.decode())
  except:
    db = contents(filename).decoded_content.decode()
  return db
