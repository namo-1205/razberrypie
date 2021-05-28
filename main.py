# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import sqlite3
import requests
import json
import serial
from picamera import PiCamera
from time import sleep

class sensor:
    def __init__(self, wei, csd, hum, tem):
        self.wei = wei
        self.csd = csd
        self.hem = hum
        self.tem = tem

try:
    ser = serial.Serial( port='COM4', baudrate=9600 )
except:
    ser.close()
    ser = serial.Serial( port='COM4', baudrate=9600 )

sensor_data = sensor(0, 0, 0, 0)

while True:
    if ser.readable():
        res = ser.readline()
        char = res.decode()[:len(res)-2] #개행문자제거

        '''
        serial.print( ,1) 모든 숫자는 소수점 1자리 가정. 
        아두이노 측 출력 예시
        Serial.print("wei: "); 출력문자는 공백 포함 5자
        Serial.print(scale.get_units()*45, 1);
        '''

        if char[:5] == 'Wei: ':
            wei = float(char[5:])
            sensor_data.wei = wei
            print('weight: ', wei )

        elif char[:5] == 'CDS: ':
            cds = float(char[5:])
            sensor_data.cds = cds
            #print('CDS_Sensor: ', cds)

        elif char[:5] == "Hum: ":
            hum = float(char[5:])
            sensor_data.hum = hum
            #print("Humidity: ", hum)

        elif char[:5] == "Tem: ":
            tem = float(char[5:])
            sensor_data.tem = tem
            #print("Temperature: ", tem)

        else:
            print("known", char[5:])


def confirm(a, bb):
    for i in bb:
        for k in i['stocks']:
            if k['name'] == a:
                return True, k['tray_id']
    return False, -1

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="http://ec2-3-36-171-69.ap-northeast-2.compute.amazonaws.com:8080/v1/graphql")

# Create a GraphQL client using the defined transport
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
files = {'file': open('./tomato.png', 'rb')} #이미지 파일 예시 -> 나중에 수정해야 함.
response = requests.post(url, files=files)
result2 = response.json()

# Execute the query on the transport
temperature = 0 #온도
weight = 0 #무게 센서 값
humidity = 0 #습도
name = result2['name'] # 재고 이름 -
light = 0 #조도센서

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
            "name": "너의 냉장고",
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
