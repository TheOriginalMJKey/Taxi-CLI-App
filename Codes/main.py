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

@bot.message_handler(commands=["my_bookings", "new_booking"])
def choose_action_passenger(message):  
    user_password = input_password[message.chat.id]  
    if message.text == '/my_bookings':
        data = sqlite3.connect('database.db')
        mycursor = data.cursor()
        mycursor.execute('SELECT * FROM orders')      
        orders = mycursor.fetchall()
        
        for order in orders:
            if order[1] == user_password:
                first_checkpoint = coords_to_address(order[2], order[3])    
                second_checkpoint = coords_to_address(order[4], order[5])  
                bot.send_message(message.chat.id, f"<i><b>Заказ №{order[0]}.</b></i>nn<i><b>Начальная точка:</b></i> {first_checkpoint}nn<i><b>Конечная точка:</b></i> {second_checkpoint}nn<i><b>Расстояние:</b></i> {order[7]} мnn<i><b>Время пути:</b></i> {order[8]} минnn<b>Цена:</b> {order[6]} ₽", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    
    elif message.text == '/new_booking':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_loca = types.KeyboardButton(text="Определить местоположение", request_location=True)
        keyboard.add(button_loca)
        mess = bot.send_message(message.chat.id, "Отправьте вашу геолокацию", reply_markup=keyboard)
        bot.register_next_step_handler(mess, geolocation, user_password, 'Пассажир')

@bot.message_handler(commands=['find_a_trip', 'settings'])
def choose_action_taxi_driver(message, user_password, teg_id):   
    if message.text == '/find_a_trip':
        data = sqlite3.connect('database.db')
        mycursor = data.cursor()
        print(user_password)
        mycursor.execute(f'SELECT * FROM taxi_drivers')
        taxi_drivers = mycursor.fetchall()
        for taxi_driver in taxi_drivers:
            if taxi_driver[1] == user_password:
                print(taxi_driver)
    
        
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_loca = types.KeyboardButton(text="Определить местоположение", request_location=True)
                keyboard.add(button_loca)
    
                mess = bot.send_message(message.chat.id, "Отправьте вашу геолокацию", reply_markup=keyboard)
                bot.register_next_step_handler(mess, geolocation, user_password, 'Таксист', manufacturer=taxi_driver[2], car_number=taxi_driver[3], src_photo_car=taxi_driver[-2])
                break

        
        
@bot.message_handler(commands=['taxi_driver', 'passanger'])
def choose_role(message, user_password):     
    if message.text == '/taxi_driver':
        mess = bot.send_message(message.chat.id, "Введите марку автомобиля.", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(mess, car_manufacturer, user_password)
        
        
    elif message.text == '/passanger':

        data = sqlite3.connect('database.db')
        mycursor = data.cursor()

        sqlFormula = "INSERT INTO passengers ('password', 'teg_id') VALUES (?,?)"
        mycursor.execute(sqlFormula, (user_password, message.chat.id))
        data.commit()
        
        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_loca = types.KeyboardButton(text="Определить местоположение", request_location=True)
        keyboard.add(button_loca)
        mess = bot.send_message(message.chat.id, "Отправьте вашу геолокацию", reply_markup=keyboard)
        bot.register_next_step_handler(mess, geolocation, user_password, 'Пассажир')

        
@bot.message_handler(content_types=['text'])              # car_manufacturer
def car_manufacturer(message, password):
    manufacturer = message.text
    mess = bot.send_message(message.chat.id, "Введите номера автомобиля.", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(mess, car_number, password, manufacturer)

    
@bot.message_handler(content_types=['text'])             # car_number
def car_number(message, password, car_manufacturer):          
    car_number = message.text
    
    mess = bot.send_message(message.chat.id, "Отправьте фото автомобиля.")    
    bot.register_next_step_handler(mess, handle_docs_photo, car_number, password, car_manufacturer)


@bot.message_handler(content_types=['photo'])    
def handle_docs_photo(message, car_number, password, car_manufacturer):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.photo[0].file_id)
        
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'cars_photos/' + car_number + '.png';     #
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_loca = types.KeyboardButton(text="Определить местоположение", request_location=True)
        keyboard.add(button_loca)
    
        mess = bot.send_message(message.chat.id, "Отправьте вашу геолокацию", reply_markup=keyboard)
        bot.register_next_step_handler(mess, geolocation, password, 'Таксист', manufacturer=car_manufacturer, car_number=car_number, src_photo_car=src)
    except:
        pass
    
    
@bot.message_handler(content_types=['text'])
def geolocation(message, password, job, manufacturer=None, car_number=None, src_photo_car=None):   
        latitude = message.location.latitude
        longitude = message.location.longitude
        dict_length = {}

        address_location = coords_to_address(longitude, latitude)    
        bot.send_message(message.chat.id, address_location, reply_markup=types.ReplyKeyboardRemove())
                         
        data = sqlite3.connect('database.db')
        mycursor = data.cursor()
        
        if job == 'Таксист':
            cnt = 0
            mycursor.execute(f'SELECT * FROM taxi_drivers')
            taxi_drivers = mycursor.fetchall()
            for driver in taxi_drivers:
                if driver[1] != password:
                    cnt += 1
            if cnt == len(taxi_drivers):
                    
                sqlFormula = "INSERT INTO taxi_drivers ('password', 'car_manufacturer', 'car_number', 'longitude', 'latitude', 'photo_car', 'teg_id') VALUES (?,?,?,?,?,?,?)"
                mycursor.execute(sqlFormula, (password, manufacturer, car_number, longitude, latitude, src_photo_car, message.chat.id))
                data.commit()

                data = sqlite3.connect('database.db')
                mycursor = data.cursor()

            mycursor.execute(f'SELECT * FROM orders')
            orders = mycursor.fetchall()
            cnt = 0
            for us in orders:
                user = us
                if cnt == 0:
                    cnt = cnt + 1
                else:
                    first_checkpoint = coords_to_address(user[2], user[3])    
                    second_checkpoint = coords_to_address(user[4], user[5])   
                    bot.send_message(message.chat.id, f"<i><b>Заказ №{user[0]}.</b></i>\n\n<i><b>Начальная точка:</b></i> {first_checkpoint}\n\n<i><b>Конечная точка:</b></i> {second_checkpoint}\n\n<i><b>Расстояние:</b></i> {user[7]} м\n\n<i><b>Время пути:</b></i> {user[8]} мин\n\n<b>Цена:</b> {user[6]} ₽", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
                
                
            
                
            mess = bot.send_message(message.chat.id, "Введите номер заказа.", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(mess, process_order_info)

         
        elif job == 'Пассажир':
            mess = bot.send_message(message.chat.id, "<b>Укажите финальный пункт назначения</b>", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(mess, set_distanation_price, password, longitude, latitude)

@bot.message_handler(content_types=['text'])
def process_order_info(message):   # num order
    num_order = message.text
    data = sqlite3.connect('database.db')
    mycursor = data.cursor()
    mycursor.execute(f'SELECT * FROM orders')
    users = mycursor.fetchall()
    passenger = []
    for us in users:              
        if us[0] == int(num_order):
            passenger.append(us)

    first_checkpoint = coords_to_address(passenger[0][2], passenger[0][3])   
    second_checkpoint = coords_to_address(passenger[0][4], passenger[0][5])   
    bot.send_message(message.chat.id, f"<i><b>Начальная точка:</b></i> {first_checkpoint}\n\n<i><b>Конечная точка:</b></i> {second_checkpoint}\n\n<i><b>Расстояние:</b></i> {passenger[0][7]} м\n\n<i><b>Время пути:</b></i> {passenger[0][8]} мин\n\n<b>Цена:</b> {passenger[0][6]} ₽", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    
    data = sqlite3.connect('database.db')
    mycursor = data.cursor()
    mycursor.execute(f'SELECT * FROM taxi_drivers WHERE teg_id={message.chat.id}')
    user_taxi = mycursor.fetchall()
    src_photo_car = user_taxi[0][6]                                                        
        
    sql = 'DELETE FROM orders WHERE id=?'
    mycursor.execute(sql, (int(num_order),))
    data.commit()
    
    
@bot.message_handler(content_types=['text'])
def set_distanation_price(message, password, longitude_start, latitude_start):   
    address_go = message.text
    longitude_end, latitude_end = [float(x) for x in address_to_coords(address_go).split(' ')]
    
    mess = bot.send_message(message.chat.id, "<b>Укажите желаемую цену в ₽.</b>", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(mess, order_compilation, password, longitude_start, latitude_start, longitude_end, latitude_end)

    
@bot.message_handler(content_types=['text'])
def order_compilation(message, password, longitude_start, latitude_start, longitude_end, latitude_end):   
    order_compilation = int(message.text)
    
    x1, y1 = longitude_start, latitude_start
    x2, y2 = longitude_end, latitude_end
    
    y = math.radians((y1 + y2) / 2)   
    x = math.cos(y)
    n = abs(x1 - x2) * 111000 * x
    n2 = abs(y1 - y2) * 111000 
    length_way = round(math.sqrt(n * n + n2 * n2))

    time_way = round(length_way / (40 * 1000) * 60)
    
    first_checkpoint = coords_to_address(longitude_start, latitude_start)
    second_checkpoint = coords_to_address(longitude_end, latitude_end)

    bot.send_message(message.chat.id, f"<i><b>Ваш заказ.</b></i>\n\n<i><b>Начальная точка:</b></i> {first_checkpoint}\n\n<i><b>Конечная точка:</b></i> {second_checkpoint}\n\n<i><b>Расстояние:</b></i> {length_way} м\n\n<i><b>Время пути:</b></i> {time_way} мин\n\n<b>Цена:</b> {order_compilation} ₽", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    
    data = sqlite3.connect('database.db')
    mycursor = data.cursor()
    sqlFormula = "INSERT INTO orders ('password', 'longitude_start', 'latitude_start', 'longitude_end', 'latitude_end', 'price', 'length_way', 'time_way', 'teg_id') VALUES (?,?,?,?,?,?,?,?,?)"
    mycursor.execute(sqlFormula, (password, longitude_start, latitude_start, longitude_end, latitude_end, order_compilation, length_way, time_way, message.chat.id))
    data.commit()
    
            
            
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
