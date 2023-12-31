from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import random
import time
import requests


def driverprepare():
    print('Загружаем драйвер...')
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    print('Драйвер загружен')
    return driver


print('Получаем список жанров с IMDB...')
driver = driverprepare()
driver.get('https://www.imdb.com/feature/genre/')
film_genres = driver.find_elements(By.CLASS_NAME, 'ipc-chip-list__scroller')[1]
genres = list(map(lambda x: x.text, film_genres.find_elements(By.TAG_NAME, 'a')))
try:
    genres.pop(genres.index('Documentary'))
except:
    pass
try:
    genres.pop(genres.index('Short'))
except:
    pass
print('Список жанров получен')
driver.close()
print('Драйвер отключён')


def weather():
    pogodastring = ''
    driver = driverprepare()
    print('Ищем погоду...')
    try:
        driver.get('https://yandex.ru/pogoda/')
        city = driver.find_element(By.XPATH, '//*[@id="main_title"]').text
        pogoda1 = driver.find_element(By.CLASS_NAME, 'fact__basic').text
        pogoda2 = driver.find_element(By.CLASS_NAME, 'fact__props').text
        pogoda = (pogoda1 + '\n' + pogoda2).split('\n')
        pogodastring = city + \
                       '\nТемпература: ' + pogoda[0] + ' (ощущается ' + pogoda[3] + ')' + \
                       '\nНебо: ' + pogoda[1] + \
                       '\nВетер: ' + pogoda[4] + \
                       '\nВлажность: ' + pogoda[5] + \
                       '\nДавление: ' + pogoda[6]
        print(pogodastring)
    except Exception as e:
        print(e)
    driver.close()
    print('Драйвер отключён')
    return pogodastring


def anekdot():
    text = ''
    driver = driverprepare()
    print('Ищем анекдот...')
    try:
        driver.get('https://www.anekdot.ru/random/anekdot/')
        anekdotes = driver.find_elements(By.CLASS_NAME, 'text')
        anekdot = random.choice(anekdotes)
        text = anekdot.text
        print(text)
    except Exception as e:
        print(e)
    driver.close()
    print('Драйвер отключён')
    return text


def movie(genre):
    poster = ''
    info = ''
    driver = driverprepare()
    print('Ищем фильмы...')
    try:
        driver.get('https://www.imdb.com/search/title/?genres=' + genre + '&explore=genres&title_type=feature')
        movies = driver.find_elements(By.CLASS_NAME, 'mode-advanced')
        print('Выбираем фильм, находим описание...')
        movie = random.choice(movies)
        info = movie.text
        info = info[info.find(' ') + 1:]
        if '\nVotes:' in info:
            info = info[:info.rfind('\nVotes:')]
        try:
            rate = info[info.find(' Rate this') - 3:info.find(' Rate this')].replace(',', '.')
            rate = round(float(rate))
        except:
            rate = 1
        info = info.replace('Rate this', '⭐️' * rate).replace('\n', '\n\n')
        print(info)
        print('Переходим по ссылке на страницу фильма...')
        link = movie.find_element(By.CLASS_NAME, 'lister-item-header').find_element(By.TAG_NAME, 'a')
        time.sleep(1)
        link.click()
        print('Перешли по ссылке, делаем паузу...')
        time.sleep(1)
        print('Извлекаем постер, устанавливаем качество картинки')
        poster = driver.find_elements(By.TAG_NAME, 'img')
        poster = poster[0].get_attribute('src')
        poster = poster[:poster.find('._V1')] + '._V1_QL75_UX1520_.jpg'
        print(poster)
    except Exception as e:
        print(e)
    driver.close()
    print('Драйвер отключён')
    return poster, info


def news():
    news = ''
    driver = driverprepare()
    print('Ищем новости...')
    try:
        driver.get('https://lenta.ru/')
        news = driver.find_element(By.CLASS_NAME, 'last24').find_elements(By.TAG_NAME, 'a')
        text = list(map(lambda x: x.text, news))
        link = list(map(lambda x: x.get_attribute('href'), news))
        news = '\n\n'.join(list(map(lambda x, y: x + '\n' + y, text, link)))
        print(news)
    except Exception as e:
        print(e)
    driver.close()
    print('Драйвер отключён')
    return news



key = 'f1bbc900ee2e50dc66bebd83f2f0a9f3'
moscowid = 524901

def currentweather(id=moscowid):
    try:
        site = 'https://api.openweathermap.org/data/2.5/weather'
        res = requests.get(site, params={'id': id, 'appid': key, 'lang': 'ru', 'units': 'metric'})
        data = res.json()
        print(data)
        city = data.get('name')
        temp = str(round(data['main']['temp'], 1)) + 'C'
        wind = str(data['wind']['speed']) + 'м/с'
        weather = data['weather'][0]['description']
        return f'Температура: {temp}\nСкорость ветра: {wind}\nПогода: {weather}'
    except Exception as e:
        print(e)

def forecastweather(id=moscowid):
    try:
        site = 'https://api.openweathermap.org/data/2.5/forecast'
        res = requests.get(site, params={'id': id, 'appid': key, 'lang': 'ru', 'units': 'metric'})
        data = res.json()
        print(data)
        forecast = ''
        for i in data['list']:
            if i['dt_txt'][11:13] == '15':
                forecast += i['dt_txt'][:10] + ' ' + \
                            str(i['main']['temp']) + 'С' + ' ' + \
                            i['weather'][0]['description'] + '\n'
        return forecast
    except Exception as e:
        print(e)