import requests

url = 'http://estella.gachon.ac.kr:8000/predict'
files = {'file': open('test.jpg', 'rb')}

r = requests.post(url, files=files)
print(r.text["result"])
