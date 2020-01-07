import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from os import makedirs
from os.path import exists
from bs4 import BeautifulSoup
import csv
from time import sleep



opt = Options()
opt.add_argument("--headless")
driver = Chrome(options = opt)
driver.get("https://wyborcza.pl/0,0.html")
try:
    driver\
        .find_element_by_xpath('//*[@id="rodoNotificationWrapper"]/div[2]/div/div[3]/button')\
        .click()
except:
    pass
driver.find_element_by_id('wH_login_form').submit()
sleep(3)

driver.find_element_by_id('wyborczaEmail').send_keys('slusarczyk1@wp.pl')
driver.find_element_by_id('wyborczaPassword').send_keys('Sraniejebanko1')
sleep(1)
driver.find_element_by_xpath('/html/body/section/section[1]/form/div[4]/button').click()
sleep(3)



def make_dir(desired_dir):
    if not exists(desired_dir):
        makedirs(desired_dir)
        
def get_data(url):
    if 'wyborcza.pl' in url:
        title = driver.find_element_by_class_name('art-title').text
        lead = driver.find_element_by_class_name('article-lead').text
        content = driver.find_element_by_class_name('art_content').text
        img_desc =  "-@@@-".join([x.text for x in driver.find_elements_by_class_name('article-image-desc')])
        comments = "-@@@-".join([x.text for x in driver.find_elements_by_class_name('cBody') if x.text != ''])
        return title, lead, content, img_desc, comments
    elif 'gazeta.pl' in url:
        title = driver.find_element_by_id('article_title').text
        lead = driver.find_element_by_id('gazeta_article_lead').text
        content = driver.find_element_by_class_name('art_content').text
        img_desc =  "-@@@-".join([x.text for x in driver.find_elements_by_class_name('desc')])
        comments = "-@@@-".join([x.find_elements_by_tag_name('p')[3].text for x in driver.find_elements_by_class_name('comment-body') if x.text != ''])
        return title, lead, content, img_desc, comments

    
    
with open('keywords', 'r') as f:
    keywords = f.read().split('\n')
    
for keyword in keywords:
    # read backed up urls 
    with open(url_dir+keyword, 'r') as f:
        urls = f.read().split('\n')
    
    # get article content
    bad_urls = []
    wyborcza_content = []
    gazeta_content = []

    for article_url in urls:
        if 'wyborcza.pl' in article_url or 'gazeta.plt' in article_url:
            driver.get(article_url)
            try:
                if 'wyborcza.pl' in article_url:
                    wyborcza_content.append(get_data(article_url))
                else:
                    gazeta_content.append(get_data(article_url))
            except:
                bad_urls.append(article_url)
    
    # save articles content for separately for wyborcza and gazeta
    articles_dir = 'data/wyborcza/articles/'
    make_dir(articles_dir)

    with open(articles_dir+keyword, 'w') as f:
        writer =  csv.writer(f)
        writer.writerows(wyborcza_content)
        
    articles_dir = 'data/gazeta/articles/'
    make_dir(articles_dir)

    with open(articles_dir+keyword, 'w') as f:
        writer =  csv.writer(f)
        writer.writerows(gazeta_content)
        
    # and save urls script had problem with
    with open(url_dir+keyword+'_errors', 'a') as f:
        f.write('\n'.join(bad_urls))
        
driver.close()