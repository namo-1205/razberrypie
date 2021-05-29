import requests

def upload_file():
  url = "http://ec2-3-36-171-69.ap-northeast-2.compute.amazonaws.com/food"
  files = {'file': open('/home/pi/Pictures/capture.jpg', 'rb')}
  response = requests.post(url, files=files)
  return response.json()