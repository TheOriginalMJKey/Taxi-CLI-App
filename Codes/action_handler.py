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
        bot.register_next_step_handler(mess, geo_location, user_password, 'Пассажир')

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
                bot.register_next_step_handler(mess, geo_location, user_password, 'Таксист', manufacturer=taxi_driver[2], car_number=taxi_driver[3], src_photo_car=taxi_driver[-2])
                break
