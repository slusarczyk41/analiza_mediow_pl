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

with open('done_fakt', 'r') as f:
    done_keywords = f.read().split('\n')
with open('keywords_pl', 'r') as f:
    raw_keywords = f.read().split('\n')
raw_keywords = [x for x in raw_keywords if x not in done_keywords]
    
    
driver.get('https://www.fakt.pl/szukaj?q=duda')
try:
    driver.find_element_by_xpath('//*[@id="Fakt"]/div[3]/div[1]/div[2]/div/div[3]/button[2]').click()
except:
    pass


for keyword in raw_keywords:
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
    
    # not_handled_urls = []
    error_urls = []
    # onet_content = []
    fakt_content = []
    error_count = 0
    
    for article_url in article_urls:
        try:
            driver.get(article_url)
            try:
                driver.find_element_by_xpath('//*[@id="mainPageBody0"]/section/div/article/main/div/div/div/a').click()
            except:
                pass
            title = driver.find_element_by_class_name('title').text.strip()
            short = driver.find_element_by_class_name('leadDetail').text.strip()
            article_body = driver.find_element_by_tag_name('article')
            try:
                long = " ".join([x.text for x in article_body.find_elements_by_class_name('hyphenate') if len(x.text.split(' ')) > 10])
            except:
                long = " ".join([x.text for x in article_body.find_elements.by_class_name('hyphenate')])
            desc = "-@@@-".join([x.text for x in driver.find_elements_by_class_name('imgDesc')])
            comments = None
            fakt_content.append([article_url, title, short, long, desc, comments])
        except Exception as e:
            print(e)
            print(article_url)
            print(driver.current_url)
            error_count += 1
            error_urls.append(article_url)
        if error_count > 100:
            break
        
    with open('data/fakt/articles/'+keyword, 'a') as f:
        writer =  csv.writer(f)
        writer.writerows(fakt_content)
    # with open('data/onet/articles/'+keyword, 'a') as f:
    #     writer =  csv.writer(f)
    #     writer.writerows(onet_content)
        
with open('data/fakt/error_urls', 'a') as f:
    f.write('\n'.join(error_urls))
# with open('data/fakt/not_handled_urls', 'a') as f:
#     f.write('\n'.join(not_handled_urls))
    
driver.close()
        
        
        
#         try:
            
#             if 'onet.pl' in article_url:
#                 if len(driver.find_elements_by_xpath('//*[@id="mainPageBody0"]/section/div/article/main/div/div/div/a')) == 1:
#                     try:
                        
#                         title = driver.find_element_by_class_name('detailTitle').text.strip()
#                         short = driver.find_element_by_class_name('leadDetail').text.strip()
#                         long = " ".join([x.text for x in driver.find_elements_by_class_name('hyphenate') if len(x.find_elements_by_tag_name('a')) == 0])
#                         desc = "-@@@-".join([x.text for x in driver.find_elements_by_class_name('imgDesc')])
#                         comments = None
                        
#                         if 'onet.pl' in driver.current_url:
#                             onet_content.append([article_url, title, short, long, desc, comments])
#                         else:
#                             fakt_content.append([article_url, title, short, long, desc, comments])
#                     except ValueError as e:
#                         error_urls.append(article_url)
#                         print(e)
                        
#                 else:
#                     not_handled_urls.append(article_url)
#             elif 'fakt.pl' in article_url:
#                 try:
#                     try:
#                         driver.find_element_by_xpath('//*[@id="mainPageBody0"]/section/div/article/main/div/div/div/a').click()
#                     except:
#                         pass
                    
#                 except Exception as e:
#                     error_urls.append(article_url)
#                     print(e)
#                     print(article_url)
#             else:
#                 not_handled_urls.append(article_url)
#         except Exception as e:
#             print(e)
#             print(article_url)
#             error_urls.append(article_url)

