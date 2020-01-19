from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException
from os import makedirs, listdir
import csv
from time import sleep


o = Options()
o.add_argument('--headless')
driver = Chrome(options = o)


driver.get('https://www.newsweek.pl/')
sleep(1)
try:
    driver.find_element_by_class_name('cmp-intro_acceptAll').click()
except:
    pass

driver.find_element_by_xpath('//*[@id="log-in-out"]').click()
sleep(2)

driver.find_element_by_xpath('//*[@id="f_login"]').send_keys('slusarczyk41@gmail.com')
driver.find_element_by_xpath('//*[@id="f_password"]').send_keys('Starehaslo1')
driver.find_element_by_xpath('//*[@id="loginForm"]/div[2]/ul[2]/li[1]/input').click()
sleep(2)

with open('keywords_pl', 'r') as f:
    keywords = f.read().split('\n')

for keyword in keywords:
    print(keyword)
    driver.get('https://www.newsweek.pl/szukaj?q='+keyword)
    urls = [
        x.get_attribute('href')
        for x in
        driver\
            .find_element_by_class_name('searchResults')\
            .find_elements_by_tag_name('a')
    ]
    print(len(urls))
    
    with open('data/newsweek/urls/'+keyword, 'w') as f:
        f.write("\n".join(urls))
    with open('data/newsweek/urls/'+keyword, 'r') as f:
        urls = f.read().split('\n')
    
    newsweek_content = []
    error_urls = []
    for url in urls:
        if 'newsweek.pl' in url:
            driver.get(url)
            try:
                newsweek_content.append([
                    driver.find_element_by_class_name('detailTitle').text.strip(),
                    driver.find_element_by_class_name('lead').text.strip(),
                    " ".join([
                        x.text
                        for x in 
                        driver\
                            .find_element_by_class_name('articleDetail')\
                            .find_elements_by_tag_name('p')
                    ])\
                        .replace('REKLAMA', '')\
                        .replace('\n', '').strip(),
                    None,
                    None
                ])
            except Exception as e:
                print('---')
                print(url)
                print(e)
                error_urls.append(url)
                
    with open('data/newsweek/articles/'+keyword, 'w') as f:
        writer =  csv.writer(f)
        writer.writerows(newsweek_content)
        
        
with open('data/newsweek/error_urls', 'w') as f:
    f.write("\n".join(error_urls))









