import requests
import json

url = 'http://estella.gachon.ac.kr:8000/predict'
files = {'file': open('test.jpg', 'rb')}

r = requests.post(url, files=files)
data = json.loads(r.text)

print(data["breed"])
print(data["prob"])
