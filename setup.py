import requests


SERVER_URL = "http://172.17.0.1:8090"

r = requests.get(f"{SERVER_URL}/index.html")
print(r)
print(r.text)
