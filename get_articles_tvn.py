import requests
from os import makedirs, listdir
from bs4 import BeautifulSoup
import csv


with open('keywords_pl', 'r') as f:
    keywords = f.read().split('\n')

all_urls = []
for filename in listdir('data/tvn/urls'):
    with open('data/tvn/urls/'+filename, 'r') as f:
        all_urls.append(f.read().split('\n'))
all_urls = set([a for b in all_urls for a in b])

print(len(all_urls))

content = []
errors = []
i = 1
for n, url in enumerate(all_urls):
    if 'tvnmeteo.' not in url and 'eurosport.' not in url:
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, features = 'html.parser').find('article')
            title = soup.find('h1').text.strip()
            if soup.find('p', 'lead-text'):
                short = soup.find('p', 'lead-text').text.strip()
                long = " ".join([
                    x.text.strip()
                    for x in
                    soup\
                        .find('div', 'article-story-content__elements')\
                        .find_all('div', 'article-element article-element--paragraph')
                ])
                imgs = "-@@@-".join([
                    x.text.strip()
                    for x in 
                    soup.find_all('div', 'inner-description__title')
                ])
            else:
                short = soup.find('h2').text.strip()
                long = " ".join(" ".join([
                    x.text.replace('\n', '').replace('\xa0', ' ').strip()
                    for x in
                    soup.find_all('p')
                ]).split())
                if long.find('if (\'undefined\' ==') != -1:
                    long = long[:long.find('if (\'undefined\' ==')]
                if soup.find('span', 'photoTitle'):
                    imgs = soup.find('span', 'photoTitle').text.strip()
                else:
                    imgs = None
            com = None
            content.append([title, short, long, imgs, com])
            
        except Exception as e:
            print(url)
            print(e)
            print('---')
            errors.append(url)
        
    if n % 1000 == 0 and n != 0:
        print(n)
        with open('data/tvn/articles/'+str(i), 'w') as f:
            writer =  csv.writer(f)
            writer.writerows(content)
            content = []
        i += 1

with open('data/tvn/error_urls', 'w') as f:
    f.write("\n".join(errors))

