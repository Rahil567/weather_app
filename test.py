import requests

API_KEY = "204feb927808f25d18197bf43d28aae3"
city = "Ahmedabad,IN"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
response = requests.get(url)
data = response.json()
print(data)  # <-- Check what you actually get

print("Temp:", data.get("main", {}).get("temp"))
print("Humidity:", data.get("main", {}).get("humidity"))