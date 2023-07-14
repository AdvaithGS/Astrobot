import requests
from os import environ
import json
#get page id from search/page and for each page, check if valid
#if valid, get the page using https://en.wikipedia.org/w/api.php?format=json&origin=*&action=query&prop=extracts&explaintext=false&exintro&pageids={pageid}
def get_wiki(query):
  l = ['atom','moon','star','space','astro','cluster','galaxy','sky','planet','solar','science','physics','scientist','cosmos']
  try:
    headers = {
      'Authorization': environ['API_KEY5'],
      'User-Agent': 'Advaith'
    }
    url = 'https://api.wikimedia.org/core/v1/wikipedia/en/search/page'
    parameters = {
      'q': query, 'limit': 1
    }
    response = requests.get(url, headers=headers, params=parameters)
    response = json.loads(response.text)
    #print(response)
    for i in response['pages']:
      #check page validity
      if any([j in i['excerpt'].lower() for j in l]):
        params = {     
          "format"      : 'json',
          'origin'      : '*',
          'action'      : 'query',
          'prop'        : 'extracts',
          'explaintext' : 'false',
          'exintro'     : '',
          'pageids'     : str(i['id']) 
        }
        req = json.loads(requests.get('https://en.wikipedia.org/w/api.php',params = params).text)['query']['pages'][str(i['id'])]['extract'].splitlines()[0]
        title = i['title']
        article_url = 'https://' + 'en' + '.wikipedia.org/wiki/' + i['key']
        image_url = ('https:' + i['thumbnail']['url']).replace('/thumb','')
        image_url = image_url[:image_url.rfind('/')]

        return title,req,article_url,image_url
  except:
    return "Error",None,None,None  