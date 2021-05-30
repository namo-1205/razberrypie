import serial
serial_channel = None
try:
  serial_channel = serial.Serial( port='/dev/ttyACM0', baudrate=9600 )
except:
  serial.close()
  serial_channel = serial.Serial( port='/dev/ttyACM0', baudrate=9600 )

class sensor:
  def __init__(self, weight, csd, humidity, temperature):
    self.weight = weight
    self.csd = csd
    self.humidity = humidity
    self.temperature = temperature

def info_from_sensor(camera, is_prev_light):
  sensor_data = sensor(0, 0, 0, 0)
  if serial_channel.readable():
    res = serial_channel.readline()
    char = res.decode()[:len(res)-2]
    if char[:5] == 'Wei: ':
      weight = float(char[5:])
      print('Weight: ', weight )
      sensor_data.weight = weight
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
      humidity = float(char[5:])
      sensor_data.humidity = humidity
      print("Humidity: ", humidity)

    elif char[:5] == "Tem: ":
      temperature = float(char[5:])
      sensor_data.temperature = temperature
      print("Temperature: ", temperature)
    else:
      print("known", char[5:])
  return (sensor_data, is_prev_light)