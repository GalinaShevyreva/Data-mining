import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

url = 'https://books.toscrape.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

response = requests.get(url, headers = headers)
soup = BeautifulSoup(response.content, 'html.parser')

release_links = []
release_cat = []
for link in soup.find_all('li'):
    try:
        release_links.append(link.find('a').get('href'))
        release_cat.append(link.find('a').getText())
    except AttributeError:
        pass

release_links = [link for link in release_links if 'category' in link]

url_joined = []
for link in release_links:
  url_joined.append(urllib.parse.urljoin(url, link))

for i in range(len(release_cat)):
    release_cat[i] = release_cat[i].replace(' ', '').replace('\n', '')
release_cat = [cat for cat in release_cat if cat != '']

categories = dict(zip(release_cat[2:-1], url_joined[1:]))

params = {'page' : 1}

books_data = []
for key, value in categories.items():
    cat_content = requests.get(value, headers = headers, params = params)
    cat_soup = BeautifulSoup(cat_content.content, 'html.parser')
    books = cat_soup.find_all('li', {'class' : "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    
    for book in books:
        title = book.h3.a['title']
        price = float(book.find('p', {'class' :"price_color"}).getText()[1:])
        details_url = url + "catalogue" + book.find("h3").find("a").get("href").replace('../../../', '/')
        details_response = requests.get(details_url, headers = headers)
        details_soup = BeautifulSoup(details_response.content, 'html.parser')     
        stock = int(details_soup.find('p', {'class': 'instock availability'}).getText(strip=True).replace('(', '').replace(')', '').split()[2])
        try:
            desc = details_soup.find('meta', {'name' : 'description'})['content']
        except:
            desc = 'None'
        
        books_data.append({
            'title' : title,
            'price' : price,
            'stock' : stock,
            'description' : desc
        })

    try:
        print(f"Обработанна страница {params['page']}")
        params['page'] += 1
    except:
        break

with open('books_data.json', 'w') as f:
     json.dump(books_data, f)

#print(books_data)
