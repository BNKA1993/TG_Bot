
import os
import telebot
from telebot import types
import random
import logging
import re
import nltk
from nltk.tokenize import word_tokenize
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('BOT_TOKEN')

logging.basicConfig(filename='bot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(token)

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
random_responses = [
    "Я не знаю, что на это ответить.",
    "Извини, я не понимаю.",
    "Может быть, попробуйте еще раз?",
    "Это интересно! А что вы думаете об этом?",
    "Пожалуйста, уточните ваш вопрос.",
    "Мне трудно дать точный ответ на это.",
    "Простите, я не могу ответить на это.",
]


@bot.message_handler(commands=['start'])
def start_message(message):
    inline_markup = types.InlineKeyboardMarkup()
    itembtn_yes = types.InlineKeyboardButton('Давай!', callback_data='yes')
    itembtn_no = types.InlineKeyboardButton('В другой раз', callback_data='no')
    inline_markup.add(itembtn_yes, itembtn_no)

    reply_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn_hello = types.KeyboardButton('Пожелания на день')
    itembtn_how_are_you = types.KeyboardButton('Как дела?')
    reply_markup.add(itembtn_hello, itembtn_how_are_you)

    bot.send_message(
        message.chat.id, 'Хай! Для начала давай я расскажу, что умею.', reply_markup=inline_markup)
    bot.send_message(message.chat.id, 'Выбери вариант:',
                     reply_markup=reply_markup)
    logger.info(f"Пользователь {message.from_user.username} запустил бота.")


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'yes':
        bot.send_message(
            call.message.chat.id, 'Я могу здороваться, спрашивать и отвечать на вопрос "Как дела?" и желать тебе хорошего дня!')
    elif call.data == 'no':
        bot.send_message(call.message.chat.id,
                         'Жаль, что ты не хочешь меня узнать:(')


@bot.message_handler(content_types=['text'])
def handle_h1(message):
    logger.info(f"Получено сообщение от пользователя { message.from_user.username}: {message.text}")
    if message.text == "Привет":
        send_random_wish(message.chat.id)
    elif message.text == "Пожелания на день":
        send_random_wish(message.chat.id)
    elif message.text == "Как дела?":
        bot.send_message(
            message.chat.id, "У меня все отлично, спасибо! Как у тебя?")
    elif message.text in ["Хорошо", "хорошо", "отлично", "Отлично", "Супер", "супер"]:
        bot.send_message(message.chat.id, "Я рад за тебя!" + "\U0001F60A")
    elif message.text in ["Плохо", "плохо", "хреново", "пойдет", "Хреново", "Пойдет", "нормально", "Норм", "Нормально"]:
        bot.send_message(message.chat.id, "Звучит печально" + "\U0001F60A")
    else:
        send_random_responses(message.chat.id)


def send_random_wish(chat_id):
    random_wish = random.choice(random_wishes)
    bot.send_message(chat_id, random_wish)
    logger.info(f"Отправлено пожелание пользователю с ID {chat_id}.")


def send_random_responses(chat_id):
    random_response = random.choice(random_responses)
    bot.send_message(chat_id, random_response)
    logger.info(f"Отправлен случайный ответ пользователю с ID {chat_id}.")


# chat_id = "236333709"  # Замените на реальный идентификатор чата пользователя
# bot.send_message(chat_id, "Бот тоже хочет внимания)))")
# logger.info(f"Отправлено сообщение пользователю А еще я так могу \U0001F60A с ID {chat_id}.")
bot.polling(none_stop=True, interval=0)
