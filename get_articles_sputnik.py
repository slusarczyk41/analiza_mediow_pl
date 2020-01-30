import requests
import csv





with open('keywords_pl', 'r') as f:
    keywords = f.read().split('\n')
    
for keyword in keywords:
    print(keyword)
    with open('data/sputnik/urls/'+keyword, 'r') as f:
        urls = f.read().split('\n')
        
    sputnik_content = []
    for url in urls:
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, features = 'html.parser')
            sputnik_content.append([
                soup.find('h1').text.strip(),
                soup.find('div', 'b-article__lead').text.strip(),
                " ".join([
                    x.text.strip()
                    for x in
                    soup.find('div', 'b-article__text').find_all('p')
                ]),
                None,
                None,
            ])
        except Exception as e:
            print(e)
            
    print(len(sputnik_content))
    with open('data/sputnik/articles/'+keyword, 'w') as f:
        writer =  csv.writer(f)
        writer.writerows(sputnik_content)