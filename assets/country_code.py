def find_country(code):
    with open ('assets/countries.txt') as f:
        for line in f.readlines():
            if code in line:
                return line.split(';')[0].title()
                