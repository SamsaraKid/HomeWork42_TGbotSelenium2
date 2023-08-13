from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

title_len = 0

# Подготовка драйвера
def driver_prepare():
    print('Загружаем драйвер...')
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    print('Драйвер загружен')
    driver.get('https://www.chitai-gorod.ru/')
    return driver


# Вывод списка книг
def print_books(books):
    for i, b in enumerate(books):
        print(str(i) + '. ' +
              b.find_element(By.CLASS_NAME, 'product-title__author').text + '. ' +
              b.find_element(By.CLASS_NAME, 'product-title__head').text + '. ' +
              b.find_element(By.CLASS_NAME, 'product-price__value').text)


# Поиск книг
def search(driver):
    global title_len  # переменная для сохранения длины предыдущего запроса
    title = input('Какую книгу хотите?\n')
    inp = driver.find_elements(By.TAG_NAME, 'input')[0]
    inp.send_keys(Keys.BACKSPACE * title_len)  # очистка предыдущего запроса
    title_len = len(title)
    inp.send_keys(title)
    inp.submit()
    time.sleep(2)
    books = driver.find_elements(By.TAG_NAME, 'article')
    # отфильтровываем книги, которые невозможно добавить в корзину
    books = list(filter(lambda x: x.find_element(By.CLASS_NAME, 'action-button').text == 'КУПИТЬ', books))
    print('Вот что есть в наличии:')
    print_books(books)
    add_to_cart(books)


# Добавление в корзину
def add_to_cart(books):
    ans = input('Купить из списка?\n'
                '\t0 - нет\n'
                '\t1 - да\n')
    if ans == '0':
        return 0
    num = int(input('Введите номер книги для добавления в корзину:\n'))
    try:
        books[num].location_once_scrolled_into_view
        time.sleep(1)
        books[num].find_element(By.CLASS_NAME, 'action-button').click()
        print('Книга добавлена в корзину')
    except:
        print('Произошла ошибка. Попробуйте ещё раз')
    add_to_cart(books)


# Просмотр корзины
def open_cart(driver):
    driver.find_element(By.CLASS_NAME, 'header-cart').click()
    time.sleep(2)
    books = driver.find_elements(By.CLASS_NAME, 'cart-item')
    print('Ваша корзина:')
    print_books(books)
    print(driver.find_element(By.CLASS_NAME, 'cart-sidebar__item-summary').text)


# Выход из магазина
def end_shopping(driver):
    print('Ждём вас снова!')
    driver.close()


# Меню
def menu(driver):
    ans = input('Что вы хотите сделать?\n'
                '\t1 - Найти книгу\n'
                '\t2 - Открыть корзину\n'
                '\t0 - Уйти из магазина\n')
    if ans == '1':
        search(driver)
    elif ans == '2':
        open_cart(driver)
    elif ans == '0':
        end_shopping(driver)
        return 0
    menu(driver)


# Основная программа
driver = driver_prepare()
print('Добро пожаловать в Читай-Город!')
menu(driver)


