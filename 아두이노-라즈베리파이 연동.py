import serial

class sensor:
    def __init__(self, wei, csd, hum, tem):
        self.weight = wei
        self.csd = csd
        self.humidity = hum
        self.temperature = tem

try:
    serial = serial_channel.Serial( port='COM4', baudrate=9600 )
except:
    serial_channel.close()
    serial = serial_channel.Serial( port='COM4', baudrate=9600 )

sensor_data = sensor(0, 0, 0, 0)    
    
while True:
    if serial_channel.readable():
        res = serial_channel.readline()
        char = res.decode()[:len(res)-2] #개행문자제거

        '''
        serial_channel.print( ,1) 모든 숫자는 소수점 1자리 가정. 
        아두이노 측 출력 예시
        serial_channel.print("wei: "); 출력문자는 공백 포함 5자
        serial_channel.print(scale.get_units()*45, 1);
        '''
        
        if char[:5] == 'Wei: ':
            wei = float(char[5:])
            sensor_data.weight = wei
            print('weight: ', wei )
            
        elif char[:5] == 'CDS: ':
            cds = float(char[5:])
            sensor_data.cds = cds
            #print('CDS_Sensor: ', cds)
            
        elif char[:5] == "Hum: ":
            hum = float(char[5:])
            sensor_data.humidity = hum
            #print("Humidity: ", hum)
            
        elif char[:5] == "Tem: ":
            tem = float(char[5:])
            sensor_data.temperature = tem
            #print("Temperature: ", tem)
        
        else:
            print("known", char[5:])

# sensor_data 클래스 반환
