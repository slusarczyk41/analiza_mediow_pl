import requests
from os import makedirs
from os.path import exists
from bs4 import BeautifulSoup




def make_dir(desired_dir):
    if not exists(desired_dir):
        makedirs(desired_dir) 

with open('keywords', 'r') as f:
    keywords = f.read().split('\n')
    
done = ['duda', 'morawiecki', 'pis', 'platforma']
    
i = 0
for keyword in keywords:
    if keyword not in done:
        print(round(i/len(keyword)*100,2))
        print(keyword)
        i += 1
        # get urls for that keyword using requests, for both wyborcza.pl and gazeta.pl
        url_dir = 'data/wyborcza_gazeta/urls/'
        urls = []

        for i in range(1, 10000):
            try:
                txt_html = requests\
                    .get("http://szukaj.gazeta.pl/wyszukaj/artykul?&query="+keyword+"&sortMode=SCORE&pageNumber="+str(i))\
                    .text
                soup = BeautifulSoup(txt_html, features = 'html.parser')

                elements = soup.find_all('section', 'elem')
                if len(elements) != 0:
                    for elem in elements:
                        a = elem.header.h3.a
                        if a:
                            urls.append(a['href'])
                else:
                    break
            except Exception as e:
                print(e)

        # save scrapped urls
        make_dir(url_dir)
        urls = list(set(urls))
        with open(url_dir+keyword, 'w') as f:
            f.write('\n'.join(urls))
