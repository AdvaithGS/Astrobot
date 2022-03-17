from os import environ
from github import Github
from time import strftime
github = Github(environ['api_key6'])
repository = github.get_user().get_repo('db')
filename = 'db'

def contents(filename = 'db'):
  return repository.get_contents(filename)

def update(db,filename = 'db'):
  content = str(db)
  sha = contents(filename).sha
  f = repository.update_file(filename, f"update file on {strftime('%H:%M %d/%m/%Y')}", content,sha)
  
def retrieve(filename = 'db'):
  try:
    db = eval(contents(filename).decoded_content.decode())
  except:
    db = contents(filename).decoded_content.decode()
  return db