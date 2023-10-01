import requests

lat = 22.52692755000000
lon = 75.92620657865751
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=c0627be1aaa1ce15d5893196f842de91"
# print(url)
print(requests.get(url).json()['main']['temp']-273)
