import serial
serial_sensor = None
try:
  serial_sensor = serial.Serial( port='/dev/ttyACM0', baudrate=9600 )
except:
  serial_sensor.close()
  serial_sensor = serial.Serial( port='/dev/ttyACM0', baudrate=9600 )

class sensor:
  def __init__(self, weightght, cds, humadity, temperature):
    self.weight = weightght
    self.cds = cds
    self.humadity = humadity
    self.temperature = temperature

_sensor_data = sensor(0, 0, 0, 0)

def info_from_sensor(camera, is_prev_light):
  if serial_sensor.readable():
    res = serial_sensor.readline()
    char = res.decode()[:len(res)-2]
    if char[:5] == 'Wei: ':
      weight = float(char[5:])
      print('weight: ', weight)
      _sensor_data.weight = weight
    elif char[:5] == 'CDS: ':
      cds = float(char[5:])
      _sensor_data.cds = cds
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
      humadity = float(char[5:])
      _sensor_data.humadity = humadity
      print("Humidity: ", humadity)

    elif char[:5] == "Tem: ":
      temperature = float(char[5:])
      _sensor_data.temperature = temperature
      print("Temperature: ", temperature)
    else:
      print("known", char[5:])
  return (_sensor_data, is_prev_light)