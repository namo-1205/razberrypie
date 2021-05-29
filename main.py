
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import sqlite3
import requests
import json
import serial
from picamera import PiCamera
from time import sleep

def confirm(a, bb):
    for i in bb:
        for k in i['stocks']:
            if k['name'] == a:
                return True, k['tray_id']
    return False, -1

class sensor:
    def __init__(self, wei, csd, hum, tem):
        self.wei = wei
        self.csd = csd
        self.hem = hum
        self.tem = tem

try:
    ser = serial.Serial( port='/dev/ttyACM0', baudrate=9600 )
except:
    ser.close()
    ser = serial.Serial( port='/dev/ttyACM0', baudrate=9600 )

sensor_data = sensor(0, 0, 0, 0)

op = 0
camera = PiCamera()
camera.start_preview()
is_prev_light = True

while True:
    if ser.readable():
        res = ser.readline()
        char = res.decode()[:len(res)-2]

        if char[:5] == 'Wei: ':
            wei = float(char[5:])
            sensor_data.wei = wei
            print('weight: ', wei )

        elif char[:5] == 'CDS: ':
            cds = float(char[5:])
            sensor_data.cds = cds
            print('CDS_Sensor: ', cds)

            if cds < 700 and is_prev_light == False: 
                camera.start_preview()
                camera.capture('/home/pi/Pictures/capture.jpg')
                is_prev_light = True
            elif cds < 700 and is_prev_light == True: 
             camera.capture('/home/pi/Pictures/capture.jpg')
            elif cds > 700 and is_prev_light == True: 
                camera.stop_preview()
                is_prev_light = False 

        elif char[:5] == "Hum: ":
            hum = float(char[5:])
            sensor_data.hum = hum
            print("Humidity: ", hum)

        elif char[:5] == "Tem: ":
            tem = float(char[5:])
            sensor_data.tem = tem
            print("Temperature: ", tem)

        else:
            print("known", char[5:])

    transport = AIOHTTPTransport(url="http://ec2-3-36-171-69.ap-northeast-2.compute.amazonaws.com:8080/v1/graphql")

    client = Client(transport=transport, fetch_schema_from_transport=True)

    con = sqlite3.connect('./test.db')

    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS stock1
                    (created_at, tray_id, name, id)''')


    query = gql(
        '''
        query{
            tray{
                id
                name
                user_id
                order_priority
                stocks{
                    created_at
                    tray_id
                    name
                    id
                }
            }
        }
        '''
    )
    result = client.execute(query)

    url = "http://ec2-3-36-171-69.ap-northeast-2.compute.amazonaws.com/food"
    files = {'file': open('/home/pi/Pictures/capture.jpg', 'rb')}
    response = requests.post(url, files=files)
    result2 = response.json()

    # Execute the query on the transport
    name = result2['name'] # 재고 이름

    insert = {}
    variables = {}

    (tf, tray_id) = confirm(name, result['tray'])

    # Execute the query on the transport
    if tf == True:
        insert = gql(
            """mutation ($object: stock_insert_input!) {
                insert_stock_one(object: $object){
                tray_id
                name
              }
            }
            """
        )

        variables = {
            "object": {
                "tray_id" : tray_id,
                "name": name
            }
        }

    else:
        insert = gql(
            """mutation ($object: tray_insert_input!) {
                insert_tray_one(object: $object){
                id
                stocks{
                  id
                }
              }
            }
            """
        )

        variables = {
            "object": {
                "name": "your refridgerator",
                "order_priority": 1,
                "user_id": 1,
                "stocks": {
                    "data": [
                        {
                            "name": name
                        }
                    ]
                }
            }
        }

    result = client.execute(insert, variable_values=variables)

    con.commit()

    result = client.execute(query)

    temperature = sensor_data.tem #온도
    weight = sensor_data.wei #무게 센서 값
    humidity = sensor_data.hum #습도
    light = sensor_data.cds #조도센서

    for i in result['tray']:
        for k in i['stocks']:
            if k['name'] == name:
                inser = gql(
                    """mutation ($object: stock_insert_input!) {
                        insert_humidity_temperature_one(object: $object){
                        stock_id
                        humidity
                        temperature
                        created_at
                      }
                    }
                    """
                )

                variables = {
                    "object": {
                        "stock_id": k[id],
                        "humidity": humidity,
                        "temperature": temperature,
                        "created_at": k['created_at']
                    }
                }

                re = client.execute(inser, variable_values=variables)

                con.commit()

                inser = gql(
                    """mutation ($object: stock_insert_input!) {
                        insert_weight_one(object: $object){
                        stock_id
                        created_at
                        value
                      }
                    }
                    """
                )

                variables = {
                    "object": {
                        "stock_id": k[id],
                        "created_at": k['created_at'],
                        "value": weight
                    }
                }


    for i in result['tray']:
        for k in i['stocks']:
            cur.execute('''INSERT INTO stock1 (created_at, tray_id, name, id)
                            VALUES (?, ?, ?, ?)''',
                        (k['created_at'],
                         i['id'],
                         k['name'],
                         k['id'])
                        )


    cur.execute('''SELECT * FROM stock1''')

    b = cur.fetchall()

    for i in b:
        print(i)

    con.close()
