@bot.message_handler(content_types=['text'])
def process_order_info(message):   
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
