from os import environ
from github import Github
from time import strftime
github = Github(environ['api_key6'])
repository = github.get_user().get_repo('db')
filename = 'db'

def contents(filename = 'db'):
  #return repository.get_contents(filename)
  pass

def update(db,filename = 'db',remarks = f"update file on {strftime('%H:%M %d/%m/%Y')}"):
  #content = str(db)
  #sha = contents(filename).sha
  #f = repository.update_file(filename, remarks, content,sha)
  pass
  
def retrieve(filename = 'db'):
  #try:
  #  db = eval(contents(filename).decoded_content.decode())
  #except:
  #  db = contents(filename).decoded_content.decode()
  #return db
  pass