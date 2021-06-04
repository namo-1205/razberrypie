from datetime import datetime
from gqlwrap import last_stock, insert_sensor_info, insert_stock_with_sensor_info, fetch_tray_info
from sqlite_file import con, cache_stock_info, get_stocks_cached
from upload_file import upload_file
from picamera import PiCamera
from serial_sensor import info_from_sensor

camera = PiCamera()
camera.start_preview()
is_prev_light = True

initial_time = datetime.now()
tray_id = 1

while True:
    now = datetime.now()
    (sensor_data, current_light) = info_from_sensor(camera, is_prev_light)
    if now.minute - initial_time.minute >= 5:
        upload_result = upload_file()

        # Execute the query on the transport
        stock_name = upload_result['name'] # 재고 이름

        last_stock_on_server = last_stock(tray_id)
        if last_stock_on_server['name'] != stock_name:
            insert_stock_with_sensor_info(stock_name, tray_id, sensor_data)
        else:
            insert_sensor_info(last_stock_on_server['id'], sensor_data)
        initial_time = datetime.now()

        result = fetch_tray_info()
        cache_stock_info(result)

        stocks = get_stocks_cached()

        for stock in stocks:
            print(stock)

con.close()
