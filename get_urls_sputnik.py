from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from os import listdir


o = Options()
o.add_argument('--headless')
o.add_argument("--no-sandbox")
o.add_argument("--disable-dev-shm-usage")
driver = Chrome(options = o)
# driver = Chrome()


with open('keywords_pl', 'r') as f:
    keywords = f.read().split('\n')
done = listdir('data/sputnik/urls/')
keywords = [x for x in keywords if x not in done]
    
for keyword in keywords:
    print(keyword)
    driver.get("https://pl.sputniknews.com/search/?query="+keyword)
    sleep(3)
    try:
        driver.find_element_by_class_name('cookie__accept').click()
    except:
        pass

    for i in range(100):
        try:
            driver.execute_script("window.scrollTo(-100, document.body.scrollHeight);")
            driver\
                .find_element_by_class_name('search')\
                .find_element_by_class_name('m-more')\
                .click()
            sleep(1.5)
        except NoSuchElementException:
            break
        else:
            pass

    urls = list(set([
        x.find_element_by_tag_name('a').get_attribute('href')
        for x in
        driver.find_elements_by_class_name('b-plainlist__title')
    ]))
    print(len(urls))

    if len(urls) > 10:
        with open('data/sputnik/urls/'+keyword, 'w') as f:
            f.write("\n".join(urls))

