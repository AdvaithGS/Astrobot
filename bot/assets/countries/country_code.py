import os
def find_country(code):
  os.chdir(os.getcwd().replace('facts','countries'))
  try:
    with open('countries.txt') as f:
      lst = f.readlines()
  except:
    with open('bot/assets/countries/countries.txt') as f:
      lst = f.readlines()
  target = ';'+code
  for line in lst:
    if target in line:
      return line.split(';')[0].title()
