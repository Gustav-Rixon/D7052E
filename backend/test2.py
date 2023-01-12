import requests

response2 = requests.post("http://127.0.0.1:1337/video_feed_terminate/0/")
response = requests.post("http://localhost:8080/")
print(response.text)
#print(response2.text)