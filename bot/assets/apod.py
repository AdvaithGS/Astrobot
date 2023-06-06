from json import loads
from requests import get
from os import environ
from bs4 import BeautifulSoup
from datetime import datetime
from assets.database.database import retrieve,update

from time import strftime, mktime
from random import randrange
def apod(date:str = None):
    db= retrieve()
    if date == None:
        if db['daily']['date'] == strftime('%Y %B %d'):
            return db['apod']
        l = 'https://apod.nasa.gov/apod/astropix.html'
    
    elif date.lower() == 'random':
        delta = mktime(datetime.now().timetuple()) - mktime(datetime(1995,6,16).timetuple())
        random_date = datetime.utcfromtimestamp(mktime(datetime(1995,6,16).timetuple()) + randrange(int(delta))).strftime('%y%m%d')
        l = f'https://apod.nasa.gov/apod/ap{random_date}.html'
    else:
        date = date.split('-')
        date = [str(int(i)%100) for i in date]
        date = ''.join(['0'*(2- len(i))+ i for i in date ])
        l = f'https://apod.nasa.gov/apod/ap{date}.html'

    
    req = get(l)
    if not req:
         return False
    soup = BeautifulSoup(req.text,'lxml')

    d = {}

    d['date'] = soup.find_all('p')[1].text.strip()

    d['video'] = bool(soup.find('iframe'))
    d['title'] = soup.find('b').text.strip()

    if d['video']:
        d['link'] = soup.find('iframe')['src']
    else:
        d['link'] = 'https://apod.nasa.gov/apod/' + soup.find_all('a')[1]['href']

    l = []
    for i in soup.find_all('center')[1].findChildren():
        if i.name == 'a':
            l.append(f'[{i.text}]({ i["href"] })')
    d['credits'] = ', '.join(l)

    d['desc'] = soup.find_all('p')[2].text.replace('\n','').strip()

    d['tomorrow'] = str(soup.find_all('center')[2].get_text)[47:]
    d ['tomorrow'] = (d['tomorrow'][d['tomorrow'].find('>',5)+1:d['tomorrow'].find('<',25)]).strip()

    return d
