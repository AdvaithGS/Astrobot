import random
def random_fact():
    with open ('assets/facts.txt') as f:
        line = random.choice(f.readlines()).split(';')
        return line[0],line[1]
