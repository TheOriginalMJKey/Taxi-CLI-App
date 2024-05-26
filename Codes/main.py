import telebot
from telebot import types
import sqlite3
import math
import sys
from io import BytesIO
import requests
from PIL import Image
import hashlib
from coords_processer import coords_to_address, address_to_coords 


token = "5356382445:AAED8i9BhPPr8NADwL66RKqcI9ZlqWN-0ok"
bot = telebot.TeleBot(token)


input_password = {} 

@bot.message_handler(commands=["help"])
def send_help_message(message):
    help_text = "\n".join([
        "/help - show this message",
        "/password - start auth or reg",
        "/register - register",
        "/auth - authenticate",
        "/my_bookings - show my bookings",
        "/new_booking - create a new booking",
        "/find_a_trip - find a trip",
        "/taxi_driver - choose a role",
        "/passanger - choose a role"
    ])
    
    bot.send_message(message.chat.id, help_text)




@bot.message_handler(commands=["start"])
def start(message):
    name = message.text
    bot.send_message(message.chat.id, "Здраствуйте <b>{first_name}</b>!".format(first_name=message.from_user.first_name), parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=["password"])
def password(message): 
    bot.send_message(message.chat.id, "Введите пароль:")
    input_password[message.chat.id] = message.text
    bot.register_next_step_handler(message, regist_and_auth)  # изменяем на message

@bot.message_handler(commands=["auth", "register"])
def regist_and_auth(message):
    if message.text == "/auth":
        data = sqlite3.connect('database.db')
        mycursor = data.cursor()
        mycursor.execute('SELECT * FROM passengers')
        passengers = mycursor.fetchall()
        for user in passengers:
            table_password = user[1]
            if table_password == input_password[message.chat.id]:
                mess = bot.send_message(message.chat.id, "Вход завершен. Здраствуйте пассажир!")
                bot.register_next_step_handler(mess, choose_action_passenger, input_password[message.chat.id], message.chat.id)
                return ''
        
        mycursor.execute('SELECT * FROM taxi_drivers')
        drivers = mycursor.fetchall()
        for user in drivers:
            table_password = user[1]
            if table_password == input_password[message.chat.id]:
                mess = bot.send_message(message.chat.id, "Вход завершен. Здраствуйте водитель!")
                bot.register_next_step_handler(mess, choose_action_taxi_driver, input_password[message.chat.id], message.chat.id)
                return ''
    
    elif message.text == '/register':
        mess = bot.send_message(message.chat.id, "Выберите вашу роль")
        bot.register_next_step_handler(mess, choose_role, input_password[message.chat.id])
