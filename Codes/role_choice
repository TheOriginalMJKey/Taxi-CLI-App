@bot.message_handler(content_types=['text'])
def choose_role(message, user_phone):  
    if message.text == 'Таксист':
        mess = bot.send_message(message.chat.id, "Введите марку машины.", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(mess, machine_firm, user_phone)
        
    elif message.text == 'Пассажир':
        mydb = sqlite3.connect('database.db')
        mycursor = mydb.cursor()
        sqlFormula = "INSERT INTO passengers ('phone', 'teg_id') VALUES (?,?)"
        mycursor.execute(sqlFormula, (user_phone, message.chat.id))
        mydb.commit()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_loca = types.KeyboardButton(text="Определить местоположение", request_location=True)
        keyboard.add(button_loca)
        mess = bot.send_message(message.chat.id, "Отправьте вашу геолокацию", reply_markup=keyboard)
        bot.register_next_step_handler(mess, geo_location, user_phone, 'Пассажир')

@bot.message_handler(content_types=['text'])  # firm
def machine_firm(message, phone):
    firm = message.text
    mess = bot.send_message(message.chat.id, "Введите номер автомобиля.", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(mess, car_numbers, phone, firm)

@bot.message_handler(content_types=['text'])  # car number
def car_numbers(message, phone, machine_firm):
    car_numbers = message.text
