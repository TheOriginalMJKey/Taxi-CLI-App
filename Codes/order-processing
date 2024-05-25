@bot.message_handler(content_types=['text'])
def process_order_info(message):  # num order
    num_order = message.text
    mydb = sqlite3.connect('database.db')
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM orders')
    users = mycursor.fetchall()
    passenger = []
    for us in users:  # find order in table by id
        if us[0] == int(num_order):
            passenger.append(us)

    first_checkpoint = coords_to_address(passenger[0][2], passenger[0][3]) 
    second_checkpoint = coords_to_address(passenger[0][4], passenger[0][5])  
    bot.send_message(message.chat.id, f"<i><b>Номер пассажира: {passenger[0][1]}.</b></i>nn<i><b>Начальная точка маршрута:</b></i> {first_checkpoint}nn<i><b>Конечная точка маршрута:</b></i> {second_checkpoint}nn<i><b>Расстояние:</b></i> {passenger[0][7]} мnn<i><b>Время пути:</b></i> {passenger[0][8]} минnn<b>Цена:</b> {passenger[0][6]} ₽", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    
    create_static_map_order(f'{passenger[0][2]},{passenger[0][3]}')

    bot.send_photo(message.chat.id, open('map_point.png', 'rb'))
    
    mycursor.execute(f'SELECT * FROM taxi_drivers WHERE teg_id={message.chat.id}')
    user_taxi = mycursor.fetchall()
    car_photo = user_taxi[0][6]  # car_photo
    bot.send_photo(passenger[0][-1], open(car_photo, 'rb'))  # passenger[0][-1] - teg_id user
    
    sql = 'DELETE FROM orders WHERE id=?'
    mycursor.execute(sql, (int(num_order),))
    mydb.commit()
    
    
@bot.message_handler(content_types=['text'])
def set_destination_price(message, phone, longitude_start, latitude_start): 
    address_go = message.text
    longitude_end, latitude_end = [float(x) for x in addess_to_coords(address_go).split(' ')]
  
    mess = bot.send_message(message.chat.id, "<b>Укажите цену.</b>", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(mess, price_way, phone, longitude_start, latitude_start, longitude_end, latitude_end)

@bot.message_handler(content_types=['text'])
def calculate_way_price(message, phone, start_longitude, start_latitude, end_longitude, end_latitude):   
    price = int(message.text)
    
    # Calculate distance
    x1, y1 = start_longitude, start_latitude
    x2, y2 = end_longitude, end_latitude
    
    avg_latitude = math.radians((y1 + y2) / 2)   
    delta_x = abs(x1 - x2) * 111000 * math.cos(avg_latitude)
    delta_y = abs(y1 - y2) * 111000 
    distance = round(math.sqrt(delta_x * delta_x + delta_y * delta_y))
    
    # Calculate time
    time_minutes = round(distance / (40 * 1000) * 60)
    
    start_point = coords_to_address(start_longitude, start_latitude)
    end_point = coords_to_address(end_longitude, end_latitude)

    bot.send_message(message.chat.id, f"<i><b>Ваш заказ.</b></i>nn<i><b>Начальная точка:</b></i> {start_point}nn<i><b>Конечная точка:</b> {end_point}nn<i><b>Расстояние:</b></i> {distance} мnn<i><b>Время пути:</b></i> {time_minutes} минnn<b>Цена:</b> {price} ₽", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    
    mydb = sqlite3.connect('database.db')
    mycursor = mydb.cursor()
    sqlFormula = "INSERT INTO orders ('phone', 'longitude_start', 'latitude_start', 'longitude_end', 'latitude_end', 'price', 'distance', 'time_minutes', 'teg_id') VALUES (?,?,?,?,?,?,?,?,?)"
    mycursor.execute(sqlFormula, (phone, start_longitude, start_latitude, end_longitude, end_latitude, price, distance, time_minutes, message.chat.id))
    mydb.commit()
