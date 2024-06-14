import requests
import json

# отправка GET-запроса на конечную точку REST API
#response = requests.get("https://ru.foursquare.com")

#parks = 16032
#museums = 10027
#coffee - 13032
#vet = 15054

from personal_data import api_key, my_client_id, my_client_secret

client_id = my_client_id
client_secret = my_client_secret

endpoint = "https://api.foursquare.com/v3/places/search"

city = input("Введите название города: ")
category = input('Введите, заведение какой категории вы ищете (парк, музей, кофейня, ветеринарная клиника): ')
if category == 'парк' or category == 'park':
    category = 16032 
elif category == 'музей'or category == 'museum':
    category = 10027
elif category == 'кофейня' or category == 'coffee':
    category = 13032
elif category == 'ветеринарная клиника' or category == 'vet':
    category = 15054
else:
    print('Категория указана неверно, скопируйте категорию из списка')

params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "near": city,
    #"query": "park"
    "categories" : category
}

headers = {
    "accept": "application/json",
    "Authorization": api_key
}

response = requests.get(endpoint, params=params,headers=headers)

if response.status_code == 200:
    print("Успешный запрос API!")
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        print("Название:", venue["name"])
        print("Адрес:", venue["location"]["address"])
        print("\n")
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)

    
