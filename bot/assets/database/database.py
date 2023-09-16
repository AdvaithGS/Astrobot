from os import environ
from github import Github
from time import strftime
github = Github(environ['API_KEY6'])
repository = github.get_user().get_repo('db')

def contents(filename):
  return repository.get_contents(filename)

def update(db,filename,remarks = f"update file on {strftime('%H:%M %d/%m/%Y')}"):
  sha = contents(filename).sha
  try:
    content = str(db)
    f = repository.update_file(filename, remarks, content,sha)
  except:
    content = str(retrieve(filename))
    f = repository.update_file(filename,remarks,content, sha)
  
def retrieve(filename:str) -> dict:
  """Returns the dictionary contained in the mentioned filename."""
  try:
    db = eval(contents(filename).decoded_content.decode())
  except:
    db = contents(filename).decoded_content.decode()
  return db
