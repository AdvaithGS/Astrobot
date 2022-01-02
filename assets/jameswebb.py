import requests
from bs4 import BeautifulSoup
from json import loads
try:
  from assets.image import get_image
except:
  from image import get_image
def binary(n):
    if n != '0' and n != 0:
        n = int(n)
        ans = []
        while n > 0:
            i = 0
            while 2**i <= n:
                i += 1
            n -= 2**(i-1)
            i -= 1
            ans.append(i)
        result = '0'*(int(ans[0]) + 1)
        for i in ans:
            result = result[:i] + '1' + result[i+1:]
    else:
        result = '0'
    return result[::-1]
def hexadecimal_to_decimal(num):
    ans = ''
    for i in num:
        if i.isdigit():
            if len(binary(i)) != 4:
                ans += '0'*(4 - len(binary(i))%4) + binary(i)
            else:
                ans += binary(i)
        else:
            alphabet = 'ABCDEF'
            if len(binary(alphabet.find(i) + 10)) != 4:
                ans += '0'*(4 - len(binary(alphabet.find(i) + 10))%4) + binary(alphabet.find(i) + 10)
            else:
                ans += binary(alphabet.find(i) + 10)
    return binary_to_decimal(ans)
def binary_to_decimal(num):
    num = num[::-1]
    ans = 0
    for i in range(len(num)):
        if num[i] == '1':
            ans += 2**i
    return ans
from time import strftime,gmtime
from datetime import datetime , timedelta
def get_james_webb():
    s = datetime.now() - timedelta(hours = 5, minutes = 30)
    d2= datetime(2020,12,25,7,30)
    s = float(round((s - d2).days%365+(s -d2).seconds/86400*24/100,2))
    #ds = '0'*(len(str(s.day))%2)
    #dh =  '0'*(len(str(s.hour))%2)
    #dm =  '0'*(len(str(s.month))%2)
    #dy = '0'*(len(str(s.year))%2)
    #s = f'{dy}{s.year}/{dm}{s.month}/{ds}{s.day}-{dh}{s.hour}:48:00' 
    s += 6.35
    req = requests.get('https://jwst.nasa.gov/content/webbLaunch/whereIsWebb.html?units=metric').text
    soup = BeautifulSoup(req,'lxml')
    page = str(soup.find_all('script')[7])
    k = s
    s -= 0.1
    while int(s*100) in range(int(k*100-50),int(k*100+50)+1) and page.find("elapsedDays':"+str(s)) == -1:
      s += 0.01
    s = round(s,2)
    print(page.find("elapsedDays':"+str(s)))
    a = page[page.find("elapsedDays':"+str(s))-200 : page.find("elapsedDays':"+str(s))+200]
    parsed = a[a.index('{'): a.rindex('}') +1].replace(',','","').replace(':','":"').replace('{','{"').replace(':.',':0.').replace('_0x1b62fa','').replace('}','"}')
    try:
      found = loads(parsed)
    except:
      pass
    daysPassed = int(float((found["'elapsedDays'"]))//1)
    hoursPassed = round((float(found["'elapsedDays'"])%1)*24)
    elapsedtime = f'{daysPassed} days and {hoursPassed} hours'
    fromEarth = float(hexadecimal_to_decimal( found["'distanceTravelledKm'"][2:] )) + float(found["'velocityKmSec'"])*(k-s)*86400
    velocity = found["'velocityKmSec'"] + ' km/s'
    tol2 = round(1446320 - fromEarth,3)
    completion = round(fromEarth/1446320*100,3)
    return elapsedtime,fromEarth,tol2,completion,get_image(),velocity
    #return velocity, fromEarth,tol2,completion
    #distance between Earth and l2 -1446320  