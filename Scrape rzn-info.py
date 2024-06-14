from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

url = "https://www.rzn.info/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

#  Добавила опции, так как получала ошибку, не проходил по ссылке.
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
browser.get(url)

# Собрала все ссылки на рубрики в этот элемент
rubric_links = browser.find_elements(By.XPATH, '//li/a[@class="rubricator__link"]')
# links = [] 
# for el in rubric_links:
#     link = el.get_attribute('href')
#     # name = el.get_attribute('text')
#     links.append(link)

# завела пустой список, куда буду подгружать словари
articles = []

i = 1 #тут начинаю с 1, потому что первая вкладка это не рубрика, а все в перемешку за 2024 год, а я хочу по темам новости собрать
while i <= 15: #по 15, а не по len(rubric_links), потому что не получается перейти на посление 3 вкладки, как будто накладывается другое окно, но я смотрю и не вижу, какое
# for rubric_link in rubric_links[1:]:
    
    # закрываем всплывающее окно про куки, которое не дает нажимать на рубрики, по двойному клику
    close_window = browser.find_element(By.XPATH, "//div/button[contains(@class, 'cookie-popup__close')]")
    close_window.click() 
    close_window.click()
    time.sleep(1) 
    # открыли все рубрики, иначе он их не видит
    all_rubrics = browser.find_element(By.XPATH, '//span/button[@type="button"]')
    all_rubrics.click()
    time.sleep(1) 
    # берем название рубрики
    link_text = rubric_links[i].text
    # переходим в нужную рубрику
    rubric_links[i].click() 
    #  скроллим вниз. так как статьи бесконечны, просто по количеству пикселей проматываю
    browser.execute_script("window.scrollBy(0,3000)")
    time.sleep(2)
    # собираем новости, которые прогрузились
    article_elements = browser.find_elements(By.XPATH, '//div/a[@class="stories-item__title-link"]')
    
    # выбираю из article_elements заголовки статей и ссылки на них
    titles = [element.text for element in article_elements]
    links = [element.get_attribute("href") for element in article_elements]

    # собираю рубрику, заголовки статей в ней и ссылки на них 
    rubric_data = {link_text: dict(zip(titles, links))}
    # print(rubric_data)
    # загружаю полученный словарь в список
    articles.append(rubric_data)
    
    # возвращаемся на главную
    browser.execute_script("window.history.go(-1)")
    time.sleep(2)  

    # обновляю переменную rubric_links, иначе не может пройти дальше 1 ссылки
    rubric_links = browser.find_elements(By.XPATH, '//li/a[@class="rubricator__link"]')
    i += 1
    # print(i)
    # 
browser.close()

# print(articles)

# записываю полученный список в json, добавила кодировку, иначе не выводились строки кириллицы
with open('articles.json', 'w', encoding='utf-8') as file:
    json.dump(articles, file, ensure_ascii=False)















# for key, value in links.items(): #Первая вкладка "все" это не вполне рубрика и я хочу ее выкинуть, чтобы собрать статьи и темам
    # if key == 'rubric':
    #     rubric = value
    # elif key == 'link':

# for link in links:
#         response = requests.get(link, headers = headers)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         browser.execute_script("window.scrollBy(0,3000)","")
#         for element in soup.find_all('//div/a[@class="stories-item__title-link"]'):
#             try:
#                 title = element.get_text()
#                 link = element.get('href')
#                 articles.append({'title' : title, 'link' : link})
#             except AttributeError:
#                 pass

        # article_title = browser.find_elements(By.XPATH, '//div/a[@class="stories-item__title-link"]')
        # article_link = browser.find_elements(By.XPATH, '//div/a[@class="stories-item__title-link"]/@href')
        # for element in article_title:
        #     title = element.get_attribute('text')
        # for element in article_link:
        #     link = element.get_attribute('href')
        # articles.append({"title": title, "article_link" : link})
    

#     name = el.get_attribute('text')
#     links.append({'rubric' : name, 'link' : link})

# print(links)

# articles = []

# for link in rubric_links:
#     link = browser.get_attribute('href')
#     link.click()
#     # rubric_title = browser.find_elements(By.XPATH,'//li/a[@class="rubricator__link"]')
#     browser.execute_script("window.scrollBy(0,3000)","")
#     article_title = browser.find_elements(By.XPATH, '//div/a[@class="stories-item__title-link"]')
#     article_link = browser.find_elements(By.XPATH, '//div/a[@class="stories-item__title-link"]/@href')
#     for element in article_title:
#         title = element.get_attribute('text')
#     for element in article_link:
#         link = element.get_attribute('href')
#     articles.append({"title": title, "article_link" : link})
# print(articles)

# with open('articles.json', 'w') as file:
#     json.dump(articles)



# url = 'https://books.toscrape.com/'


# response = requests.get(url, headers = headers)
# soup = BeautifulSoup(response.content, 'html.parser')
