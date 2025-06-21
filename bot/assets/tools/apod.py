from requests import get
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from assets.database.database import retrieve
from disnake import Embed,Color
from time import strftime, mktime
from random import randrange
def apod(date:str = '') -> dict:
    db_daily= retrieve('daily')
    if date == '':
        if db_daily['date'] == strftime('%Y %B %d'):
            return db_daily
        l = 'https://apod.nasa.gov/apod/astropix.html'
    
    elif date.lower() == 'random':
        delta = mktime(datetime.now().timetuple()) - mktime(datetime(1995,6,16).timetuple())
        random_date = datetime.fromtimestamp(mktime(datetime(1995,6,16).timetuple()) + randrange(int(delta)),tz = timezone.utc).strftime('%y%m%d')
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

    d['date'] = soup.find_all('p')[1].text
    d['date'] = d['date'][:d['date'].find('<')].strip()

    d['video'] = bool(soup.find('iframe'))
    d['title'] = soup.find('b').text.strip()

    if d['video']:
        d['link'] = soup.find('iframe')['src']
    else:
        d['link'] = 'https://apod.nasa.gov/apod/' + soup.find_all('a')[1]['href']

    l = []
    for i in soup.find_all('center')[1].findChildren():
        if i.name == 'a' and i.text != 'Copyright':
            l.append(f'[{i.text}]({ i["href"] })')
    d['credits'] = ', '.join(l)

    d['desc'] = soup.find_all('p')[2].text.replace('\n',' ').strip().strip('Explanation : ')

    d['tomorrow'] = soup.find_all('center')[2].text.split('\n')[5].split(':')[-1].strip().title()
    
    return d

def get_embed(d : dict) -> dict:
    d['desc'] = f'''{d['date']}\nDiscover the cosmos!\n\n{d['desc']}\n\n{('Credits: '+ d['credits']) if 'credits' in d else ''}'''
    embed = Embed(title=d['title'], url=d['link'], description=d['desc'], color= Color.orange(),timestamp = datetime.now());

    embed.set_footer(text=f"Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.\nTomorrow's image: {d['tomorrow']}")
      
    return {"date":d['date'],"embed":embed,'video':d['video'],'link':d['link']}