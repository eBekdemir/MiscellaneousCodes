import requests as req
from bs4 import BeautifulSoup as bs
import cloudscraper
import sys
sys.stdout.reconfigure(encoding='utf-8')


output = ''

def decode_cf_email(cf_email):
    r = int(cf_email[:2], 16)
    email = ''.join([chr(int(cf_email[i:i + 2], 16) ^ r) for i in range(2, len(cf_email), 2)])
    return email


res = req.get("https://www.legal500.com/c/turkey/directory").text

soup = bs(res, 'html.parser')

div = soup.find('div', class_='grid grid-cols-1 gap-5 md:gap-6 lg:grid-cols-4')

articles = div.find_all('article')

h4s = [article.find('h4', class_='typography-heading-xs') for article in articles]

ass = []
for a_tag in h4s:
    a = a_tag.find('a', href=True)
    ass.append(a['href'])

for link in ass:
    try:

        scraper = cloudscraper.create_scraper()
        url = f'https://www.legal500.com{link[:-8]}contact'
        con_page = scraper.get(url).text
        
        soup = bs(con_page, 'html.parser')
        
        city = soup.find('div', class_='text-accent typography-eyebrow').text
        name = soup.find('h1', class_='text-balance typography-heading-xl').text
        div = soup.find('div', class_='px-0 xl:container xl:mx-auto')
        links = div.find_all('span', class_='__cf_email__')
        email = []
        for lnk in links:
            data = lnk['data-cfemail']
            mail = decode_cf_email(data)
            if '@' in mail:
                email.append(mail)
        if len(email) != 0:
            output = '; '.join(email) + '\n'
            if 'istanbul' in city.lower() or 'ıstanbul' in city.lower():
                with open('istanbul.txt', 'a', encoding='UTF-8') as file:
                    file.write(output)
            with open('details.txt', 'a', encoding='UTF-8') as file:
                file.write(f'{city.ljust(18)}\t{name.ljust(36)}\t{output}')
    except:
        print('error')