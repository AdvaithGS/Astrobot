import random
import os
def random_fact():
  #changes directory from main.py directory to assets/facts
  os.chdir(os.getcwd().replace('countries','facts'))
  #opens facts.txt file and gets a random fact from it using random library
  try:
    with open ('bot/assets/facts/facts.txt',encoding = 'utf-8') as f:
        line = random.choice(f.readlines()).split(';')
  except:
    with open ('facts.txt',encoding='utf-8') as f:
      #facts.txt is a delimited file with ; as delimiting character
      line = random.choice(f.readlines()).split(';')
  return line