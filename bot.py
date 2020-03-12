from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import vk_api
import requests
import time
import random
from bs4 import BeautifulSoup as bs
import apiai
import json
df_key = 'f8e942456803467e862e8b2edc2772fc'
vk_session= vk_api.VkApi(token = '')
help_=('Здравствуйте, в данном разделе вы можете прочесть всю информацию о чат-боте Саня и посмотреть ответы на часто задаваемые вопросы.\n Как запустить работу чат-бота? \n Нажите кнопку "Начать", которая находится в меню чат-бота или же просто напишите "Начать" и бот автоматически начнет свою работу. \n Как долго будет выполняться поиск ближайших мест для перекуса? \n Обычно это занимает не более 5 минут.')
spisok1=['Привет, я помогу тебе найти кафе и рестораны на любой вкус! Чтобы я нашел места для перекуса, напиши "Найди кафе"' , 'Привет! Я создан для того, чтобы находить кафе, где вы сможете вкусно поесть. Для того, чтобы найти рестораны и кафе, напиши "Найди кафе"', 'Здравствуй, друг! Я твой персональный помощник для поиска кафе и ресторанов. Чтобы найти самые подходящие рестораны, напиши "Найди кафе"']
spisok2=['Выполняю поиск самых близких кафе по Вашему местоположению...','Буквально через минуту будет готов список самых популярных кафе...', 'Осталось совсем чуть-чуть...', 'Ищу для тебя идеальное кафе...']
spisok3=['Выберите категорию кафе, которая Вам подходит: \n1- фастфуд/ пиццерии/ бары \n 2- рестораны/ кафе',' В каком месте Вам сегодня хочется оказаться? \n1- фастфуд/ пиццерии/ бары \n 2- рестораны/ кафе','Какие места мне показать? \n1- фастфуд/ пиццерии/ бары \n 2- рестораны/ кафе']
spisok4=['Нашли то, что искали? Всегда рад помочь!','Спасибо, что обратился ко мне! Жду тебя снова!)', 'Ну вот и все, обращайся, если снова понадобиться найти для себя кафе!']
from vk_api.longpoll import VkLongPoll, VkEventType
longpoll= VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type== VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text == 'Найди кафе' or event.text == 'найди кафе' or event.text == 'Привет' or event.text == 'привет':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message='Привет! Напиши что хочешь покушать', random_id=time.time() * 10000)
                for event1 in longpoll.listen():
                    if event1.type == VkEventType.MESSAGE_NEW and event1.to_me and event1.text:
                        stroka = event1.text.split()
                        query = '+'.join(stroka)
                        html_code = requests.get('https://www.afisha.ru/msk/restaurants/restaurant_list/?q='+query).text
                        soup = bs(html_code, 'lxml')
                        for product in soup.findAll('section', {'class': 'places_cards'}):
                            product_name = product.find('span', {'class': 'places_name'}).text
                            product_adress = product.find('span', {'class': 'places_address'}).text
                            product_link = product.a.get('href')
                            if product_name or product_adress:
                                try:
                                    vk.messages.send(user_id = event.user_id, message = product_name + product_adress + ('https://www.afisha.ru/' + product_link), random_id = time.time() * 10000)
                                except:
                                    vk.messages.send(user_id=event.user_id, message='Не удалось вывести данные об этом ресторане',random_id=time.time() * 10000)
        elif event.text:
            if event.from_user:
                ai_req = apiai.ApiAI(df_key).text_request()
                ai_req.lang = 'ru'
                ai_req.session_id = '123'
                ai_req.query = event.text
                responseJson = json.loads(ai_req.getresponse().read().decode('utf-8'))
                response = responseJson['result']['fulfillment']['speech']
                if response:
                    answer = response
                else:
                    answer = 'всё плохо'
                vk.messages.send(user_id=event.user_id, message=answer, random_id=time.time() * 10000)