from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException
from os import makedirs, listdir
import csv
from time import sleep



o = Options()
o.add_argument('--headless')
o.add_argument("--no-sandbox")
o.add_argument("--disable-dev-shm-usage")
driver = Chrome(options = o)
# driver = Chrome()

with open('done_onet', 'r') as f:
    done_keywords = f.read().split('\n')
with open('keywords_pl', 'r') as f:
    raw_keywords = f.read().split('\n')
keywords = [x for x in raw_keywords if x not in done_keywords]

onet_keywords = {
    'sąd+najwyższy': 'sad-najwyzszy',
    'imigranci': 'imigracja',
    'ekologia': 'ekologia',
    'emigracja': 'emigracja',
    'pis': 'pis',
    'platforma': 'po',
    'duda': 'andrzej-duda',
    'morawiecki': 'mateusz-morawiecki',
    'szydło': 'beata-szydlo',
    'kaczyński': 'jaroslaw-kaczynski',
    'kwaśniewski': 'aleksander-kwasniewski',
    'lewica': 'lewica',
    'prawica': 'prawica',
    'lgbt': 'lgbt',
    'unia+europejska': 'unia-europejska',
    'rosja': 'rosja',
    'stany': 'stany-zjednoczone',
    'premier': 'premier',
    'prezydent': 'prezydent',
    'opozycja': 'opozycja',
    'rząd': 'rzad',
    'sejm': 'sejm',
    'polska': 'polska',
    'putin': 'putin',
    'trump': 'donald-trump',
    'ukraina': 'ukraina',
    'media': 'media',
    'bank': 'banki',
    'niemcy': 'niemcy',
    'papież': 'papiez',
    'kościół': 'kosciol',
    'korwin': 'korwin',
    'rydzyk': 'tadeusz-rydzyk',
    'feminizm': 'feminizm',
    'leszek+miller': 'leszek-miller',
}

driver.get('https://wiadomosci.onet.pl/')
try:
    driver\
        .find_element_by_class_name('cmp-intro_options')\
        .find_elements_by_tag_name('button')[1].click()
except:
    pass

# def get_last_url():
#     return driver.find_elements_by_class_name('listItem')[-1]\
#             .find_elements_by_tag_name('a')[-1]\
#             .get_attribute('href')


for keyword in keywords:
    print(keyword)
    onet_keyword = onet_keywords[keyword]
    driver.get('https://wiadomosci.onet.pl/'+onet_keyword)
    
    last_url = ''
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for more_button in driver\
                            .find_element_by_class_name('pageContent')\
                            .find_elements_by_class_name('more'):
            try:
                more_button.click()
            except Exception as e:
                pass
        sleep(1)

    urls = [
        x.find_elements_by_tag_name('a')[-1].get_attribute('href')
        for x in 
        driver.find_elements_by_class_name('listItem')
    ]
    
    with open('data/onet/urls/'+keyword, 'w') as f:
        f.write("\n".join(urls))

    with open('data/onet/urls/'+keyword, 'r') as f:
        urls = f.read().split('\n')
    print(len(urls))
    if len(urls) < 25:
        keywords.append(keyword)
        driver.close()
        driver = Chrome(options = o)
        continue

    error_count = 0
    error_urls = []
    onet_content = []
    for url in urls:
        driver.get(url)
        try:
            title = driver.find_element_by_class_name('mainTitle').text.strip()
            short = driver.find_element_by_id('lead').text.strip()
            long = " ".join([
                x.text.replace('REKLAMA\n', '')
                for x in 
                driver.find_element_by_id('detail').find_elements_by_class_name('hyphenate')
            ][:-1])
            img = " ".join([
                x.text
                for x in 
                driver.find_elements_by_class_name('imageDescription')
            ])
            com = None
            onet_content.append([
                url, title, short, long, img, com
            ])
        except:
            error_count = error_count + 1
            if error_count > 10:
                error_count = 0
                driver.close()
                sleep(3)
                driver = Chrome(options = o)
                sleep(3)
            error_urls.append(url)
    print(len(onet_content))
    with open('data/onet/articles/'+keyword, 'w') as f:
        writer =  csv.writer(f)
        writer.writerows(onet_content)

with open('data/onet/error_urls', 'w') as f:
    f.write("\n".join(error_urls))




