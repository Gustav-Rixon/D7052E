import requests

response = requests.post("http://localhost:8080/", data="argument=value")
print(response.text)