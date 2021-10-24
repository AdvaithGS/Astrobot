def find_country(code):
    target = ';'+code
    with open ('assets/countries.txt') as f:
        for line in f.readlines():
            if target in line:
                return line.split(';')[0].title()
                