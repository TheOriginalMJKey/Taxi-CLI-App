import sqlite3
import sys
import math
import requests
from io import BytesIO
from PIL import Image

token = "5356382445:AAED8i9BhPPr8NADwL66RKqcI9ZlqWN-0ok
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    name = message.text
    bot.send_message(message.chat.id, "Привет <b>{first_name}</b>! Пожалуйста, отправьте свой номер телефона. Используйте команду /phone".format(first_name=message.from_user.first_name), parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=["phone"])
def phone(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    user_markup.add(button_phone)
    msg = bot.send_message(message.chat.id, "Пожалуйста, предоставьте системе ваш номер телефона", reply_markup=user_markup)
    bot.register_next_step_handler(msg, regist_and_auth)
