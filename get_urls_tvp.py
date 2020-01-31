import requests
from bs4 import BeautifulSoup
import re
from os import listdir


done = listdir('data/tvp/urls')
with open('keywords_pl', 'r') as f:
    keywords = f.read().split('\n')
keywords = [x for x in keywords if x not in done]

for keyword in keywords:
    print(keyword)
    keyword_urls = []
    for i in range(1, 151):
        if i % 20 == 0: print(i)
        r = requests.get('https://www.tvp.info/szukaj?query=s%C4%85d+naj&page='+str(i))
        soup = BeautifulSoup(r.text, features = 'html.parser')
        
        js = [
            x
            for x in
            soup.find_all('script')
            if '"items"' in str(x)
        ][0].text
        
        urls = [
            'https://wiadomosci.tvp.pl'+x.replace('https:\\/\\/wiadomosci.tvp.pl', '').replace('\\','')
            for x in
            re.findall(r'"url" : "(.*?)",', js)
        ]
        
        # print(len(urls))
        if len(urls) != 0:
            keyword_urls.append(urls)
        else:
            break
        
    keyword_urls = [x for y in keyword_urls for x in y]
    print(len(keyword_urls))
    
    with open('data/tvp/urls/'+keyword, 'w') as f:
        f.write("\n".join(keyword_urls))