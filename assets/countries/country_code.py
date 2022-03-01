def find_country(code):
    target = ';'+code
    try:
      with open ('assets/countries/countries.txt') as f:
          for line in f.readlines():
              if target in line:
                  return line.split(';')[0].title()
    except:
      with open('countries.txt') as f:
          for line in f.readlines():
            if target in line:
              return line.split(';')[0].title()       