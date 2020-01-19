from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException
from os import makedirs, listdir
import csv
from time import sleep

tvn_keywords = {
    'sąd+najwyższy': 'najwyższy',
    'imigranci': 'imigranci',
    'ekologia': 'ekologia',
    'emigracja': 'emigracja',
    'pis': 'pis',
    'platforma': 'platforma',
    'duda': 'duda',
    'morawiecki': 'morawiecki',
    'szydło': 'szydło',
    'kaczyński': 'kaczyński',
    'kwaśniewski': 'kwaśniewski',
    'lewica': 'lewica',
    'prawica': 'prawica',
    'lgbt': 'lgbt',
    'unia+europejska': 'europejska',
    'rosja': 'rosja',
    'stany': 'zjednoczone',
    'premier': 'premier',
    'prezydent': 'prezydent',
    'opozycja': 'opozycja',
    'rząd': 'rząd',
    'sejm': 'sejm',
    'polska': 'polska',
    'putin': 'putin',
    'trump': 'trump',
    'ukraina': 'ukraina',
    'media': 'media',
    'bank': 'bank',
    'niemcy': 'niemcy',
    'papież': 'papież',
    'kościół': 'kościół',
    'korwin': 'korwin',
    'rydzyk': 'rydzyk',
    'feminizm': 'feminizm',
    'leszek+miller': 'miller',
}

o = Options()
o.add_argument('--headless')
driver = Chrome(options = o)
# driver = Chrome()

driver.get('https://tvn24.pl/szukaj.html?q=duda&r=1&p=1')
try:
    driver.find_element_by_xpath('//*[@id="rodoLayer"]/div/div[3]/a[2]').click()
except:
    pass

with open('keywords_pl', 'r') as f:
    keywords = f.read().split('\n')
with open('done_urls_tvn', 'r') as f:
    done_keywords = f.read().split('\n')
keywords = [x for x in keywords if x not in done_keywords]

error_count = 0
for keyword in keywords:
    print(keyword)
    tvn_keyword = tvn_keywords[keyword]
    driver.get('https://tvn24.pl/szukaj.html?q='+tvn_keyword+'&r=1&p=1&page=2')
    
    no_pages = int(int(driver.find_element_by_xpath('//*[@id="tvn24"]/div[2]/div/div[3]/div[4]/div[1]/span').text[1:-1])/10)
    if no_pages > 500:
        no_pages == 500
    
    all_urls = []
    for i in range(1, no_pages):
        try:
            driver.get('https://tvn24.pl/szukaj.html?q='+tvn_keyword+'&r=1&p=1&page='+str(i))
            all_urls.append([
                x.find_element_by_tag_name('a').get_attribute('href')
                for x in 
                driver\
                   .find_element_by_class_name('searchResult')\
                   .find_elements_by_class_name('news')
            ])
        except:
            error_count = error_count + 1
            if error_count > 100:
                break
    keyword_urls = [a for x in all_urls for a in x]
    
    with open('data/tvn/urls/'+keyword, 'w') as f:
        f.write("\n".join(keyword_urls))
