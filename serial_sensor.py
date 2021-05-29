import serial
try:
  ser = serial.Serial( port='/dev/ttyACM0', baudrate=9600 )
except:
  ser.close()
  ser = serial.Serial( port='/dev/ttyACM0', baudrate=9600 )

class sensor:
  def __init__(self, wei, csd, hum, tem):
    self.wei = wei
    self.csd = csd
    self.hem = hum
    self.tem = tem

def info_from_sensor(camera, is_prev_light):
  sensor_data = sensor(0, 0, 0, 0)
  if ser.readable():
    res = ser.readline()
    char = res.decode()[:len(res)-2]
    if char[:5] == 'Wei: ':
      wei = float(char[5:])
      print('weight: ', wei )
      sensor_data.wei = wei
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
  return (sensor_data, is_prev_light)