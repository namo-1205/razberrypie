from datetime import datetime
from graphql import receive_tray_id, new_stock_info, insert_sensor_info, fetch_tray_info
from sqlite_file import con, cache_stock_info, get_stocks_cached
from upload_file import upload_file
from picamera import PiCamera
from serial_sensor import info_from_sensor

camera = PiCamera()
camera.start_preview()
is_prev_light = True

initial_time = datetime.now()

while True:
    upload_result = upload_file()

    # Execute the query on the transport
    stock_name = upload_result['name'] # 재고 이름

    tray_id = receive_tray_id(stock_name)

    # Execute the query on the transport

    new_stock_info(tray_id, stock_name)

    now = datetime.now()

    (sensor_data, current_light) = info_from_sensor(camera, is_prev_light)

    if now.minute - initial_time.minute >= 5:
        insert_sensor_info(stock_name, sensor_data)
        initial_time = datetime.now()

    result = fetch_tray_info()
    cache_stock_info(result)

    stocks = get_stocks_cached()

    for stock in stocks:
        print(stock)

con.close()
