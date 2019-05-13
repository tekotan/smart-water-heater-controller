import requests

r = requests.get("http://127.0.0.1:5000/1/1/1/high/1")
print(r.text)
