from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import random
import time

genres = ['Action', 'Animation', 'Comedy', 'Crime', 'Drama', 'Fantasy', 'Horror', 'Sci-Fi']

def driverprepare():
    print('Загружаем драйвер...')
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    print('Драйвер загружен')
    return driver


def weather():
    pogodastring = ''
    driver = driverprepare()
    print('Ищем погоду...')
    try:
        driver.get('https://yandex.ru/pogoda/moscow')
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
        info = info[:info.rfind('\n')]
        info = info.replace('Rate this', '★').replace('\n', '\n\n')
        print(info)

        print('Переходим по ссылке на страницу фильма...')
        link = movie.find_element(By.CLASS_NAME, 'lister-item-header').find_element(By.TAG_NAME, 'a')
        time.sleep(1)
        link.click()
        print('Перешли по ссылке, делаем паузу...')
        time.sleep(1)

        print('Переходим по ссылке на постер фильма...')
        driver.find_elements(By.CLASS_NAME, 'ipc-lockup-overlay')[0].click()
        print('Извлекаем постер...')
        poster = driver.find_elements(By.TAG_NAME, 'img')[0].get_attribute('src')
        print(poster)
    except Exception as e:
        print(e)
    driver.close()
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
    return news