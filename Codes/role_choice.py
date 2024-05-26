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
