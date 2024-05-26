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
            bot.register_next_step_handler(mess, choose_order)

         
        elif job == 'Пассажир':
            mess = bot.send_message(message.chat.id, "<b>Укажите финальный пункт назначения</b>", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(mess, set_distanation_price, password, longitude, latitude)
