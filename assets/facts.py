import random
def random_fact():
  try:
    with open ('assets/facts.txt',encoding = 'utf-8') as f:
        line = random.choice(f.readlines()).split(';')
        return line
  except:
    with open ('facts.txt',encoding = 'utf-8') as f:
        line = random.choice(f.readlines()).split(';')
        return line