import telebot
import botlib

# читаем токен из файла
file = open('token', 'r')
token = file.readline()
file.close()

# создаём бота
bot = telebot.TeleBot(token)
print('Бот создан')

# создаём кнопки клавиатуры в чате
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.add(telebot.types.InlineKeyboardButton(text='🌤 Погода', callback_data='weather'),
             telebot.types.InlineKeyboardButton(text='🤦 Анекдот', callback_data='anekdot'))
keyboard.add(telebot.types.InlineKeyboardButton(text='🎞 Фильм', callback_data='movie'),
             telebot.types.InlineKeyboardButton(text='📰 Новости', callback_data='news'))
# создаём кнопки с жанрами
btns = []
btns_row = []
for i in range(len(botlib.genres)):
    btns_row.append(telebot.types.InlineKeyboardButton(text=botlib.genres[i], callback_data=botlib.genres[i]))
    if (i + 1) % 3 == 0 or i == len(botlib.genres) - 1:
        btns.append(btns_row)
        btns_row = []
keyboard_movie = telebot.types.InlineKeyboardMarkup(btns)

# создаём кнопки меню
markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row('/start', '/stop')


# старт бота
@bot.message_handler(commands=['start'])
def start_mes(info):
    print(info.from_user.username, 'послал(а) команду /start')
    bot.send_message(info.chat.id, 'Добро пожаловать в бота-помощника', reply_markup=markup)  # создаём меню
    bot.send_message(info.chat.id, 'Выберите команду', reply_markup=keyboard)  # выводим клавиатуру в чате


# скрываем меню
@bot.message_handler(commands=['stop'])
def stop_mes(info):
    print(info.from_user.username, 'послал(а) команду /stop')
    markup_hide = telebot.types.ReplyKeyboardRemove()
    bot.send_message(info.chat.id, '/start для возобновления работы', reply_markup=markup_hide)


# обработка команд от кнопок в чате
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    print(call.from_user.username, 'послал(а) команду', call.data)
    try:
        if call.data == 'weather':
            bot.send_message(call.message.chat.id, 'Проверяю погоду...')
            bot.send_message(call.message.chat.id, botlib.weather())
            bot.send_message(call.message.chat.id, 'Выберите команду', reply_markup=keyboard)
        elif call.data == 'anekdot':
            bot.send_message(call.message.chat.id, 'Ищу анекдот...')
            bot.send_message(call.message.chat.id, botlib.anekdot())
            bot.send_message(call.message.chat.id, 'Выберите команду', reply_markup=keyboard)
        elif call.data == 'movie':
            bot.send_message(call.message.chat.id, 'Выберите жанр', reply_markup=keyboard_movie)
        elif call.data in botlib.genres:
            bot.send_message(call.message.chat.id, 'Ищу фильм...')
            poster, info = botlib.movie(call.data)
            bot.send_photo(call.message.chat.id, poster, info)
            bot.send_message(call.message.chat.id, 'Выберите команду', reply_markup=keyboard)
        elif call.data == 'news':
            bot.send_message(call.message.chat.id, 'Ищу новости...')
            bot.send_message(call.message.chat.id, botlib.news())
            bot.send_message(call.message.chat.id, 'Выберите команду', reply_markup=keyboard)
        else:
            mes = 'Неверная команда'
            bot.send_message(call.message.chat.id, mes)
    except Exception as e:
        print(e)
        bot.send_message(call.message.chat.id, 'Произошла ошибка, попробуйте ещё раз')
        bot.send_message(call.message.chat.id, 'Выберите команду', reply_markup=keyboard)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)

