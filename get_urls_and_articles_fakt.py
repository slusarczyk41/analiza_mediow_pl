from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException
from os import makedirs, listdir
import csv
from time import sleep



o = Options()
o.add_argument('--headless')
driver = Chrome(options = o)
# driver = Chrome()


done_keywords = listdir('data/fakt/urls')
with open('keywords_pl', 'r') as f:
    raw_keywords = f.read().split('\n')
keywords = [x for x in raw_keywords if x not in done_keywords]
    
    
driver.get('https://www.fakt.pl/szukaj?q=duda')
try:
    driver.find_element_by_xpath('//*[@id="Fakt"]/div[3]/div[1]/div[2]/div/div[3]/button[2]').click()
except:
    pass


for keyword in keywords:
    print(keyword)
    driver.get('https://www.fakt.pl/szukaj?q='+keyword)
    
    err_count = 0
    for i in range(150):
        try:
            driver.find_element_by_class_name('bottomarrow').click()
        except ElementNotInteractableException:
            sleep(1)
            err_count = err_count + 1
            continue
        sleep(3)

        if err_count > 20:
            break
            
    result_elements = driver.find_element_by_class_name('searchResults')\
      .find_elements_by_tag_name('a')
    result_links = [x.get_attribute('href') for x in result_elements if x.get_attribute('href') != None]
    print(result_links)
            
    with open('data/fakt/urls/'+keyword, 'a') as f:
        f.write('\n'.join(result_links))
        
    with open('data/fakt/urls/'+keyword, 'r') as f:
        article_urls = list(set(f.read().split('\n')))
    
    not_handled_urls = []
    error_urls = []
    onet_content = []
    fakt_content = []
    
    for article_url in article_urls:
        try:
            driver.get(article_url)
            if 'onet.pl' in article_url:
                if len(driver.find_elements_by_xpath('//*[@id="mainPageBody0"]/section/div/article/main/div/div/div/a')) == 1:
                    try:
                        if 'onet.pl' in driver.current_url:
                            driver.find_element_by_xpath('//*[@id="mainPageBody0"]/section/div/article/main/div/div/div/a').click()
                            title = driver.find_element_by_class_name('detailTitle').text.strip()
                            short = driver.find_element_by_class_name('leadDetail').text.strip()
                            long = " ".join([x.text for x in driver.find_elements_by_class_name('hyphenate') if len(x.find_elements_by_tag_name('a')) == 0])
                            desc = "-@@@-".join([x.text for x in driver.find_elements_by_class_name('imgDesc')])
                            comments = None
                            onet_content.append([article_url, title, short, long, desc, comments])
                        else:
                            title = driver.find_element_by_class_name('title').text.strip()
                            short = driver.find_element_by_class_name('detailTitle').text.strip()
                            article_body = driver.find_element_by_class_name('articleBody')
                            long = " ".join([x.text for x in article_body.find_elements_by_class_name('hyphenate') if len(x.text.split(' ')) > 10])
                            desc = "-@@@-".join([x.text for x in driver.find_elements_by_class_name('imgDesc')])
                            comments = None
                            fakt_content.append([article_url, title, short, long, desc, comments])
                    except:
                        error_urls.append(article_url)
                else:
                    not_handled_urls.append(article_url)
            elif 'fakt.pl' in article_url:
                try:
                    title = driver.find_element_by_class_name('title').text.strip()
                    short = driver.find_element_by_class_name('detailTitle').text.strip()
                    article_body = driver.find_element_by_class_name('articleBody')
                    long = " ".join([x.text for x in article_body.find_elements_by_class_name('hyphenate') if len(x.text.split(' ')) > 10])
                    desc = "-@@@-".join([x.text for x in driver.find_elements_by_class_name('imgDesc')])
                    comments = None
                    fakt_content.append([article_url, title, short, long, desc, comments])
                except:
                    error_urls.append(article_url)
            else:
                not_handled_urls.append(article_url)
        except:
            error_urls.append(article_url)
            
    with open('data/fakt/articles/'+keyword, 'a') as f:
        writer =  csv.writer(f)
        writer.writerows(fakt_content)
    with open('data/onet/articles/'+keyword, 'a') as f:
        writer =  csv.writer(f)
        writer.writerows(onet_content)
        
with open('data/fakt/error_urls', 'a') as f:
    f.write('\n'.join(error_urls))
with open('data/fakt/not_handled_urls', 'a') as f:
    f.write('\n'.join(not_handled_urls))
    
driver.close()
