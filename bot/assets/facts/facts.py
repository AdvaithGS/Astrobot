import random
import os
def random_fact():
  os.chdir(os.getcwd().replace('countries','facts'))
  try:
    with open ('bot/assets/facts/facts.txt',encoding = 'utf-8') as f:
        line = random.choice(f.readlines()).split(';')
  except:
    with open ('facts.txt',encoding='utf-8') as f:
        line = random.choice(f.readlines()).split(';')
  return line