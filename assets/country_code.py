def find_country(code):
    with open ('countries.txt') as f:
        for line in f.readlines():
            if code in line:
                return line.split(';')[0]
                