import requests
from os import environ
import json
#get page id from search/page and for each page, check if valid
#if valid, get the page using https://en.wikipedia.org/w/api.php?format=json&origin=*&action=query&prop=extracts&explaintext=false&exintro&pageids={pageid}
def get_wiki(query):
  l = ['atom','moon','star','space','astro','cluster','galaxy','sky','planet','solar','science','physics','scientist','cosmos']
  try:
    headers = {
      'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIwYmUzMTZmZWQ0Zjk2OWJmMWJkNzljMjhlNTkzZGFkOCIsImp0aSI6IjYwNTMwMjVmZjQ2MDMyNGI4MjJhMDFhNjdmYTBiYWViNGZhMjUxN2E4YjBhMWNkN2Q5MTQ3YWZmMmM3MzM5MTRjN2FhMGZiYTlmYzcwYzkzIiwiaWF0IjoxNjQ0NDk3NzA5LCJuYmYiOjE2NDQ0OTc3MDksImV4cCI6MzMyMDE0MDY1MDksInN1YiI6IjY4OTAxNDQ3IiwiaXNzIjoiaHR0cHM6XC9cL21ldGEud2lraW1lZGlhLm9yZyIsInJhdGVsaW1pdCI6eyJyZXF1ZXN0c19wZXJfdW5pdCI6NTAwMCwidW5pdCI6IkhPVVIifSwic2NvcGVzIjpbImJhc2ljIl19.V_O-EMNu1A9J8EXAiXAWNOiAoyBGTeqT3EW8-lQrD2Mj6UmfFBFcU1kblqC87s7mlN5ySFWwt1h4MBrm0GBEZBXZz4_AElBkq80-v0FS-J68EWe-dymhqVC9ZYs_uQ-mQuOu89Q_tpaly-7kJKkue06t5swVEHi4ME-qOSHzaBmQXMQCIUztICynVFFqdmAl-wQiM3km10uWC7Hm7t4I6fsAcOtaZc5HmHvitjM2gsTvhP0VPXqS466OslR9FJiyHYLM-9BR4yaGiOxsAOyKWixaycEqdVtQJb-6YNBPIH86AG9bs7_-QCrUZe-1BVQPbIZMAosejuzUPP6y485hvhNljEhIcsSf3lgjRcrouBBlVqhhX-z9J5h5c6P6XKYdKQ3rEo11rkiFwwqcu9MTMVyL09ZbXFNEwc3DbukBm6VhhW6-uD2SgnMjuKJQdi8WODH_RcEpg7vuL2BfQg_o4ZH3IFbL56azoOx2LTV72o6oQ-7uppLRzxrorY1rA86jF6ZRCz6BQyUWdQhVlyfaFJsWHQ6zzOk8GmZkspskNDTWBXl2NLWcqTSDOdY5_eVWBgCqUDD0HXAvBkX5WVWa-SI9NhE5hY5z1a7yu6sgPxSIulYFT2YZuCaO4vM5z83SusQJI3ObYSinBnxuRt3BOaWbPD-f0RxOjAlEnAEkvMs",
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