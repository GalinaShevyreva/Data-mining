import requests
from lxml import html
import csv

url = 'https://nonews.co/directory/lists/countries/killer'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
#строка агента моего браузера

response =requests.get(url, headers = headers)
# получаю содержимое страницы
tree = html.fromstring(html=response.content)
# парсим содержимое переменной responce
all_countries = [] #тут я по образцу из приложенного файла делаю пустой список, в который запишу все полученные данные

countries18 = tree.xpath(".//div[2]/div/article/div[2]/div/div[1]/table/tbody/tr")
countries13 = tree.xpath(".//div[2]/div/article/div[2]/div/div[4]/table/tbody/tr") 
# чтобы данные не смешивались и позднее их можно было разметить по годам, я выгружаю данные из каждой таблицы отдельно. 
# Можно было бы выгрузить и все 4 таблицы, но за 2015 и 2016 годы данных почти нет, не увидела смысла.

for country in countries18:
    m = {
        'position' : int(country.xpath(".//td[contains(@class, 'column-1')]/text()")[0]),
        'name' : country.xpath(".//td[contains(@class, 'column-2')]/text()")[0],
        'kills_qty' : int(country.xpath(".//td[contains(@class, 'column-3')]/text()")[0]),
        'year' : 2018
    }

    all_countries.append(m)
# формирую словарь из таблицы за 18 год и загружаю его в список

for country in countries13:
    m = {
        'position' : int(country.xpath(".//td[contains(@class, 'column-1')]/text()")[0]),
        'name' : country.xpath(".//td[contains(@class, 'column-2')]/text()")[0],
        'kills_qty' : float(country.xpath(".//td[contains(@class, 'column-3')]/text()")[0]),
        'year' : 2013
    }

    all_countries.append(m)
# формирую словарь из таблицы за 13 год и загружаю его в список. 
# Таким образом у нас в списке будут данные по странам за 13 и 18 годы с пометкой, в каком именно год они собраны.

print(all_countries)

with open('killers_by_countries.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['position', 'name', 'kills_qty', 'year'])
    writer.writeheader()
    for country in all_countries:
        writer.writerow(country)

# теперь полученный список со словарями записан в csv файл, где можно будет дальше обрабатывать данные.
# С ним я тоже поигралась, файл будет приложен к домашке.