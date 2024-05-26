@bot.message_handler(content_types=['text'])
def geolocation_order(message, phone, role, firm=None, car_numbers=None, car_photo=None):  
    latitude = message.location.latitude
    longitude = message.location.longitude
    dict_length = {}

    address_location = coords_to_address(longitude, latitude)  
    bot.send_message(message.chat.id, address_location, reply_markup=types.ReplyKeyboardRemove())

    mydb = sqlite3.connect('database.db')
    mycursor = mydb.cursor()

    if role == 'Таксист':
        cnt = 0
        mycursor.execute('SELECT * FROM taxi_drivers')
        taxi_drivers = mycursor.fetchall()
        for driver in taxi_drivers:
            if driver[1] != phone:
                cnt += 1
        if cnt == len(taxi_drivers):
            sqlFormula = "INSERT INTO taxi_drivers ('phone', 'machine_firm', 'car_numbers', 'longitude', 'latitude', 'car_photo', 'teg_id') VALUES (?,?,?,?,?,?,?)"
            mycursor.execute(sqlFormula, (phone, firm, car_numbers, longitude, latitude, car_photo, message.chat.id))
            mydb.commit()

    mycursor.execute('SELECT * FROM orders')
    orders = mycursor.fetchall()
    for i in orders:
        user = i
        first_checkpoint = coords_to_address(user[2], user[3])  
        second_checkpoint = coords_to_address(user[4], user[5])  
        bot.send_message(message.chat.id, f"<i><b>Заказ №{user[0]}.</b></i>nn<i><b>Начальная точка:</b></i> {first_checkpoint}nn<i><b>Конечная точка:</b></i> {second_checkpoint}nn<i><b>Расстояние:</b></i> {user[7]} мnn<i><b>Время пути:</b></i> {user[8]} минnn<b>Цена:</b> {user[6]} ₽", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

    if role == 'Таксист':
        mess = bot.send_message(message.chat.id, "Введите номер заказа.", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(mess, choose_order)

    elif role == 'Пассажир':
        mess = bot.send_message(message.chat.id, "<b>Укажите конечную точку маршрута</b>", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(mess, where_go, phone, longitude, latitude)
