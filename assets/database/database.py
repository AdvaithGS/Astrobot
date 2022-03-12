from os import environ
from github import Github
from time import strftime
from hashlib import sha1
github = Github(environ['api_key6'])
repository = github.get_user().get_repo('db')
filename = 'db'
def update(db):
  content = str(db)
  sha = repository.get_contents(filename).sha
  f = repository.update_file(filename, f"update file on {strftime('%H:%M %d/%m/%Y')}", content,sha)
def retrieve():
  db = eval(repository.get_contents(filename).decoded_content.decode())
  return db