import serial

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

# sensor_data 클래스 반환
