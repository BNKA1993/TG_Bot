
import os  # импорт модуля для взаимодействия с ОС
import telebot  # импорт библиотеки для работы с Telegram Bot API в Python
from telebot import types  # импорт модуля из библиотеки Telebot, для фич интерфейса
import random  # импорт модуля для выбора рандомных значений
import logging  # импорт модуля для системы логирования
import datetime

# возможность загрузки переменных среды из файла .env
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('BOT_TOKEN')  # получение значение токена бота

logging.basicConfig(filename='bot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)  # подключение системы логирования

bot = telebot.TeleBot(token)

# список пожеланий для пользователя, которые отправляются рандомно
random_wishes = [
    "Привет! Желаю тебе замечательного дня!",
    "Привет! Пусть у тебя все будет прекрасно!",
    "Привет! Пускай удача сопутствует тебе во всем!",
    "Привет! Желаю улыбок и радости каждый день!",
    "Привет! Пусть сегодня будет особенным для тебя днем!",
    "Привет! Зарядись позитивом и силами на весь день!",
    "Привет! Желаю тебе море позитивных эмоций и успехов!",
    "Привет! Пусть этот день принесет тебе много радости!"
]

# список ответов для пользователя, которые отправляются рандомно
random_responses = [
    "Я не знаю, что на это ответить.",
    "Извини, я не понимаю.",
    "Может быть, попробуйте еще раз?",
    "Это интересно! А что вы думаете об этом?",
    "Пожалуйста, уточните ваш вопрос.",
    "Мне трудно дать точный ответ на это.",
    "Простите, я не могу ответить на это.",
]

# определение функции обработки команды /start от пользователя


@bot.message_handler(commands=['start'])
def start_message(message):
    # создание объекта со встроенной клавиатурой
    inline_markup = types.InlineKeyboardMarkup()
    itembtn_yes = types.InlineKeyboardButton(
        'Давай!', callback_data='yes')  # создание кнопки "Давай!"
    itembtn_no = types.InlineKeyboardButton(
        'В другой раз', callback_data='no')  # создание кнопки "В другой раз"
    # добавление созданных кнопок в объект inline_markup
    inline_markup.add(itembtn_yes, itembtn_no)

    # создание объекта с обычной клавиатурой
    reply_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    # создание кнопки "Пожелания на день" для обычной клавиатуры
    itembtn_hello = types.KeyboardButton('Пожелания на день')
    itembtn_random_photo = types.KeyboardButton('Котэ')
    # создание кнопки "Как дела?" для обычной клавиатуры
    itembtn_how_are_you = types.KeyboardButton('Как дела?')
    # Добавление кнопки "Сегодняшнее число"
    today_button = types.KeyboardButton('Текущая дата')
    # добавление созданных кнопок в объект reply_markup
    reply_markup.add(itembtn_hello, itembtn_how_are_you,
                     today_button, itembtn_random_photo)

    # отправка сообщения пользователю с приветственным сообщением и встроенной клавиатурой
    bot.send_message(
        message.chat.id, 'Хай! Для начала давай я расскажу, что умею.', reply_markup=inline_markup)
    # отправка еще одного сообщение с текстом "Выбери вариант:" и обычной клавиатурой
    bot.send_message(message.chat.id, 'Выбери вариант:',
                     reply_markup=reply_markup)
    # запись информации о том, что пользователь запустил бота в лог

    logger.info(f"Пользователь {message.from_user.username} запустил бота.")


# Определяем функцию-обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # Проверяем значение поля data в callback-запросе
    if call.data == 'yes':
        # Если значение равно 'yes', отправляем сообщение пользователю с подтверждением
        bot.send_message(
            call.message.chat.id, 'Я умею спрашивать и отвечать на вопрос "Как дела?"\nПоказывать текущую дату\nОтправлять пожелания на день')
    # Если значение равно 'no', отправляем сообщение пользователю с сожалением
    elif call.data == 'no':
        bot.send_message(call.message.chat.id,
                         'Жаль, что ты не хочешь меня узнать:(')


# Определяем функцию-обработчик текстовых сообщений

@bot.message_handler(content_types=['text'])
def handle_h1(message):
    # Записываем информацию о полученном сообщении в лог
    logger.info(f"Получено сообщение от пользователя {
                message.from_user.username}: {message.text}")
    # Проверяем текст сообщения
    if message.text == "Привет":
        # Если сообщение "Привет", отправляем случайное пожелание
        send_random_wish(message.chat.id)
    elif message.text == "Пожелания на день":
        # Если сообщение "Пожелания на день", также отправляем случайное пожелание
        send_random_wish(message.chat.id)
    elif message.text == "Как дела?":
        # Если сообщение "Как дела?", отправляем ответ о состоянии бота
        bot.send_message(
            message.chat.id, "У меня все отлично, спасибо! Как у тебя?")
    elif message.text == "Текущая дата":
        send_today_message(message.chat.id)
    elif message.text == "Котэ":
        send_random_photo(message.chat.id)
    elif message.text in ["Хорошо", "хорошо", "отлично", "Отлично", "Супер", "супер"]:
        # Если сообщение соответствует одному из вариантов хорошего состояния, отправляем поздравление
        bot.send_message(message.chat.id, "Я рад за тебя!" + "\U0001F60A")
    elif message.text in ["Плохо", "плохо", "хреново", "пойдет", "Хреново", "Пойдет", "нормально", "Норм", "Нормально"]:
        # Если сообщение соответствует одному из вариантов плохого состояния, отправляем сочувствие
        bot.send_message(message.chat.id, "Звучит печально" + "\U0001F60A")
    else:
        # Если сообщение не соответствует ни одному из вышеуказанных, отправляем случайный ответ
        send_random_responses(message.chat.id)


def send_today_message(chat_id):
    # Получаем текущую дату
    today_date = datetime.date.today()
    # Отправляем сообщение с текущей датой
    bot.send_message(chat_id, f"Сегодня {today_date}")


# Определяем функцию для отправки случайного пожелания

def send_random_wish(chat_id):
    # Выбираем случайное пожелание из списка
    random_wish = random.choice(random_wishes)
    # Отправляем пожелание пользователю по указанному chat_id
    bot.send_message(chat_id, random_wish)
    # Записываем информацию о пожелании в лог
    logger.info(f"Отправлено пожелание пользователю с ID {chat_id}.")


# Определяем функцию для отправки случайного ответа

def send_random_responses(chat_id):
    # Выбираем случайный ответ из списка
    random_response = random.choice(random_responses)
    # Отправляем случайный ответ пользователю по указанному chat_id
    bot.send_message(chat_id, random_response)
    # Записываем информацию о случайном ответе в лог
    logger.info(f"Отправлен случайный ответ пользователю с ID {chat_id}.")


def send_random_photo(chat_id):
    bot.send_animation(
        chat_id, f'https://cataas.com/cat/gif?rnd={random.random()}')


try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    print(f"Ошибка при запуске бота: {e}")


# # chat_id = "236333709"  # Замените на реальный идентификатор чата пользователя
# # bot.send_message(chat_id, "Бот тоже хочет внимания)))")
# # logger.info(f"Отправлено сообщение пользователю А еще я так могу \U0001F60A с ID {chat_id}.")
# bot.polling(none_stop=True, interval=0)
