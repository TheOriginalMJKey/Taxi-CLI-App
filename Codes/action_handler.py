@bot.message_handler(content_types=['text'])
def choose_action_passenger(message, user_phone, teg_id):  # passenger action handlеr
    if message.text == 'Мои поездки':
        mydb = sqlite3.connect('database.db')
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM orders')
        orders = mycursor.fetchall()
        for order in orders:
            if order[1] == user_phone:
                first_checkpoint = coords_to_address(order[2], order[3])  
                second_checkpoint = coords_to_address(order[4], order[5])  
                bot.send_message(message.chat.id, f"<i><b>Заказ №{order[0]}.</b></i>n<i><b>Начальная точка:</b></i> {first_checkpoint}n<i><b>Конечная точка:</b></i> {second_checkpoint}n<i><b>Расстояние:</b></i> {order[7]} мn<i><b>Время пути:</b></i> {order[8]} минn<b>Цена:</b> {order[6]} ₽", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    
    elif message.text == 'Новая поездка':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_loca = types.KeyboardButton(text="Определить местоположение", request_location=True)
        keyboard.add(button_loca)
        mess = bot.send_message(message.chat.id, "Отправьте вашу геолокацию", reply_markup=keyboard)
        bot.register_next_step_handler(mess, geo_location, user_phone, 'Пассажир')


@bot.message_handler(content_types=['text'])
def choose_action_taxi_driver(message, user_phone, teg_id):  # taxi driver action handler
    if message.text == 'Выбрать поездку':
        mydb = sqlite3.connect('database.db')
        mycursor = mydb.cursor()
        mycursor.execute(f'SELECT * FROM taxi_drivers')
        taxi_drivers = mycursor.fetchall()
        for taxi_driver in taxi_drivers:
            if taxi_driver[1] == user_phone:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_loca = types.KeyboardButton(text="Определить местоположение", request_location=True)
                keyboard.add(button_loca)
                mess = bot.send_message(message.chat.id, "Отправьте вашу геолокацию", reply_markup=keyboard)
                bot.register_next_step_handler(mess, geo_location, user_phone, 'Таксист', firm=taxi_driver[2], car_numbers=taxi_driver[3])
                break