import requests
from json import loads
from bs4 import BeautifulSoup
from os import environ


l = ['atom','moon','star','space','astro','cluster','galaxy','sky','planet','solar','science','physic','scientist','cosmos']
def clean(text):
    while '[' in text:
        text = text.replace(text[text.find('['):text.find(']',text.find('['))+1],'')
    return text
def get_wiki(search_query):
    if len(search_query.split()) == 1:
        search_query = search_query.capitalize()
    not_space = False
    try:
        headers = {
                'Authorization': environ['api_key5'],
                'User-Agent': 'Advaith'
                }
        page = f'https://en.wikipedia.org/w/rest.php/v1/page/{search_query}/html'
        req = requests.get(page).text
        soup = BeautifulSoup(req,'lxml')
        d = {}
        try:
            if 'refer to' in soup.find_all('p')[1].text:
                x = d['13']
            text = soup.find_all('p')[0].text
            i = 1
            while len(text) < 100:
                text = soup.find_all('p')[i].text
                i += 1
            
            if any([z in text.lower() for z in l]):
                text = clean(text)
                correct = True
            else:
                not_space = True
                correct = False
        except:
            if ('refer' in soup.find_all('p')[0].text or 'refer' in soup.find_all('p')[1].text or  'other' in soup.find_all('p')[0].text or 'other' in soup.find_all('p')[1].text):
                for i in soup.find_all('a'):
                    if any([z in i.text.lower() for z in l]):
                        search_query = i['href'][1:]
                        page = 'https://en.wikipedia.org/w/rest.php/v1/page' + i['href'][1:] + '/html'
                        req = requests.get(page).text
                        soup = BeautifulSoup(req,'lxml')
                        i = 1
                        text = soup.find_all('p')[0].text
                        while len(text) < 100:
                            text = soup.find_all('p')[i].text
                            i += 1
                        text = clean(text) 
                        correct = True
                        break
                else:
                    correct = False
          
        if correct:
            url = 'https://api.wikimedia.org/core/v1/wikipedia/en/search/page'
            parameters = {'q': search_query, 'limit': 1}
            response = loads(requests.get(url, headers=headers, params=parameters).text)
            image = 'https:' + response['pages'][0]['thumbnail']['url'].replace('200px','500px')
            try:
                desc = clean(soup.find('div', attrs = {'class':'infobox-caption'}).text)
            except:
                try:
                    desc = clean(soup.find('figcaption').text)
                except:
                    desc = search_query
        else:
            image =  None
    except:
        pass
    try:
        return text,image,desc
    except:
        if not_space:
            return None,None,'Not space'
        else:
            return None,None,'Not found'





