from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from os import makedirs, listdir
from os.path import exists
import csv
from time import sleep



def make_dir(desired_dir):
    if not exists(desired_dir):
        makedirs(desired_dir)
        
def get_data(url):
    if 'wyborcza.pl' in url:
        try:
            title = driver.find_element_by_xpath('//*[@id="art-header"]/div[2]/h1').text
        except:
            try:
                title = driver.find_element_by_class_name('art-title').text
            except:
                try:
                    title = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/header/div[2]').text
                except:
                    try:
                        title = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/header/div[2]/h1').text
                    except:
                        try:
                            title = driver.find_element_by_xpath('/html/body/main/div[1]/div/header/div[2]/h1').text
                        except:
                            try:
                                title = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/header/div[2]/h1').text
                            except:
                                try:
                                    title = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/header/div[2]').text
                                except:
                                    title = None
        try:
            lead = driver.find_element_by_class_name('article-lead').text
        except:
            try:
                lead = driver.find_element_by_xpath('//*[@id="pagetype_art"]/div[4]/div[2]/section/article/section').text
            except:
                lead = None
        try:
            content = driver.find_element_by_id('artykul').text
        except:
            content = driver.find_element_by_class_name('art_content').text
        img_desc =  "-@@@-".join([x.text for x in driver.find_elements_by_class_name('article-image-desc')])
        comments = "-@@@-".join([x.text for x in driver.find_elements_by_class_name('cBody') if x.text != ''])
        return [title, lead, content, img_desc, comments]
    elif 'gazeta.pl' in url:
        title = driver.find_element_by_xpath('//*[@id="article_title"]').text
        try:
            lead = driver.find_element_by_id('gazeta_article_lead').text
        except:
            try:
                lead = driver.find_element_by_xpath('//*[@id="gazeta_article_lead"]').text
            except:
                lead = None
        try:
            content = driver.find_element_by_id('artykul').text
        except:
            content = driver.find_element_by_class_name('art_content').text
        img_desc =  "-@@@-".join([x.text for x in driver.find_elements_by_class_name('desc')])
        comments = "-@@@-".join([x.find_elements_by_tag_name('p')[3].text for x in driver.find_elements_by_class_name('comment-body') if x.text != ''])
        return [title, lead, content, img_desc, comments]


# prepare urls
url_dir = 'data/wyborcza_gazeta/urls/'
with open('keywords', 'r') as f:
    keywords = f.read().split('\n')

all_urls = []
for collected_url_file in listdir(url_dir):
    if 'ipynb' not in collected_url_file:
        with open(url_dir+collected_url_file, 'r') as f:
            tmp_urls = f.read().split('\n')
        for tmp_url in tmp_urls:
            all_urls.append(tmp_url)
all_urls = list(set(all_urls))
print(len(all_urls))
all_urls = [x for x in all_urls if x != '']
all_urls = [x for x in all_urls if 'gazeta.pl' in x or 'wyborcza.pl' in x]
print(len(all_urls))


# initialize selenium
opt = Options()
opt.add_argument("--headless")
opt.add_argument("--no-sandbox")
opt.add_argument("--disable-dev-shm-usage")
driver = Chrome(options = opt)
# driver = Chrome()
driver.get("https://wyborcza.pl/0,0.html")
try:
    driver\
        .find_element_by_xpath('//*[@id="rodoNotificationWrapper"]/div[2]/div/div[3]/button')\
        .click()
except:
    pass
driver.find_element_by_id('wH_login_form').submit()

driver.find_element_by_id('wyborczaEmail').send_keys('slusarczyk1@wp.pl')
driver.find_element_by_id('wyborczaPassword').send_keys('Sraniejebanko1')
driver.find_element_by_xpath('/html/body/section/section[1]/form/div[4]/button').click()
sleep(1)


# get article content
bad_urls = []
wyborcza_content = []
gazeta_content = []
i = 70
error_counter = 0
for n, article_url in enumerate(all_urls[71000:]):
    # getpage
    try:
        driver.get(article_url)
        if 'gazeta.pl' in driver.current_url:
            gazeta_content.append([article_url] + get_data(driver.current_url))
        elif 'wyborcza.pl' in driver.current_url:
            wyborcza_content.append([article_url] + get_data(driver.current_url))
    except Exception as e:
        error_counter = error_counter + 1
        print(e)
        print(article_url)
        print('----')
        try:
            driver.close()
        except:
            pass
        try:
            driver = Chrome(options = opt)
        except:
            pass
        bad_urls.append(article_url)
        if error_counter > 1200:
            break
    # every x pages save to new file good and bad ones
    if n % 1000 == 0:
        i += 1
        
        articles_dir = 'data/gazeta/articles/'
        make_dir(articles_dir)
        with open(articles_dir + str(i), 'w') as f:
            writer =  csv.writer(f)
            writer.writerows(gazeta_content)
            
        articles_dir = 'data/wyborcza/articles/'
        make_dir(articles_dir)
        with open(articles_dir + str(i), 'w') as f:
            writer =  csv.writer(f)
            writer.writerows(wyborcza_content)

        gazeta_content = []
        wyborcza_content = []
    
with open('data/wyborcza_gazeta/article_errors', 'w') as f:
    f.write('\n'.join(bad_urls))
    
driver.close()
