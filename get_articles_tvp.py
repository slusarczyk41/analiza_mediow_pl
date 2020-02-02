import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException
from os import makedirs, listdir
from os.path import exists
from bs4 import BeautifulSoup
import csv
from time import sleep
from bs4 import element
import re


files = []
for filename in listdir('data/tvp/urls/'):
    with open('data/tvp/urls/'+filename, 'r') as f:
        files.append(f.read().split('\n'))

urls = list(set([x for y in files for x in y]))
len(urls)

articles_list = []
i = 1
for n, url in enumerate(urls):
    try:
        r = requests.get(url.replace('.pl', '.info').replace('wiadomosci.', ''))
        soup = BeautifulSoup(r.text)
        articles_list.append([
            soup.find('h1').text.strip(),
            soup.find('p', 'am-article__heading article__width').text.strip(),
            " ".join([
                x.text.replace('\n', '').replace('\t', '').replace('\r', '').replace('#wieszwiecejPolub nas', '').strip()
                for x in
                soup.find_all('p', 'am-article__text article__width')
            ]),
            None,
            None,
        ])
        print('done')
    except Exception as e:
        print(url, e)
        
    if n % 1000 == 0 and n != 0:
        print(len(articles_list))
        with open('data/tvp/articles/'+str(i), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(articles_list)
        articles_list = []
        i += 1
        


