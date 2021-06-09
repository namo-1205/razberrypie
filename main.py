from datetime import datetime
from gqlwrap import last_stock, insert_sensor_info, insert_stock_with_sensor_info, fetch_tray_info, insert_notification
from sqlite_file import con, cache_stock_info, get_stocks_cached, get_created_at_cached, already_notified, get_too_old_stocks
from upload_file import upload_file
from picamera import PiCamera
from serial_sensor import info_from_sensor
import time

camera = PiCamera()
camera.start_preview()
is_prev_light = True

initial_time = datetime.now()
tray_id = 1

while True:
    now = datetime.now()

    (sensor_data, current_light) = info_from_sensor(camera, is_prev_light)
    if (now - initial_time).total_seconds() >= 300:
        upload_result = upload_file()

        # Execute the query on the transport
        stock_name = upload_result['name'] # 재고 이름
        stock_image_address = upload_result['key']

        last_stock_on_server = last_stock(tray_id)
        if last_stock_on_server['name'] != stock_name:
            insert_stock_with_sensor_info(stock_name, tray_id, sensor_data, stock_image_address)
        else:
            insert_sensor_info(last_stock_on_server['id'], sensor_data, stock_image_address)
        initial_time = datetime.now()

        result = fetch_tray_info()
        cache_stock_info(result)

        stocks = get_stocks_cached()

        for stock in stocks:
            print(stock)
    too_old_stocks = get_too_old_stocks()
    for (_, tray_id, name, stock_id) in too_old_stocks:
        notified = already_notified(stock_id, '저장량')
        if not notified:
            insert_notification(tray_id, stock_id, name, "저장량")
con.close()