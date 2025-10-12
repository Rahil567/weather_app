import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# -----------------------------
# Load API key from .env
# -----------------------------
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# -----------------------------
# Load historical weather data
# -----------------------------
data = pd.read_csv('india_2000_2024_daily_weather.csv')
print("✅ Data loaded successfully!")
print(data.head())

# -----------------------------
# Data cleaning
# -----------------------------
for col in data.select_dtypes(include=['float64', 'int64']).columns:
    data[col] = data[col].fillna(data[col].mean())

for col in data.select_dtypes(include=['object']).columns:
    data[col] = data[col].fillna(data[col].mode()[0])

le = LabelEncoder()
for col in data.select_dtypes(include=['object']).columns:
    data[col] = le.fit_transform(data[col])

print("✅ Data cleaned successfully!")

# -----------------------------
# Rainfall distribution plot
# -----------------------------
plt.figure(figsize=(8,4))
data['rain_sum'].plot(kind='hist', bins=30, title='Rainfall Distribution')
plt.xlabel('Rainfall (mm)')
plt.show()

# -----------------------------
# Define features and target
# -----------------------------
features = ['temperature_2m_max', 'temperature_2m_min', 'apparent_temperature_max',
            'apparent_temperature_min', 'precipitation_sum', 'wind_speed_10m_max',
            'wind_gusts_10m_max', 'wind_direction_10m_dominant', 'weather_code']

X = data[features]
y = (data['rain_sum'] > 0).astype(int)

print("Features and target variable defined successfully!")
print("Features (X) shape:", X.shape)
print("Target (y) shape:", y.shape)

# -----------------------------
# Train model
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)
print("✅ Model trained successfully!")
print("🎯 Model Accuracy:", round(accuracy_score(y_test, model.predict(X_test)) * 100, 2), "%\n")

# -----------------------------
# Function to get live weather and predict
# -----------------------------
def get_live_weather_and_prediction(city="Ahmedabad"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data_live = response.json()

    temp = data_live['main']['temp']
    temp_min = data_live['main']['temp_min']
    temp_max = data_live['main']['temp_max']
    humidity = data_live['main']['humidity']
    pressure = data_live['main']['pressure']
    wind_speed = data_live['wind']['speed']

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("============================================")
    print("🌍 Live Weather Data for", city)
    print("🕒 Time:", now)
    print(f"Temperature: {temp}°C (min {temp_min} / max {temp_max})")
    print("Humidity:", humidity, "%")
    print("Pressure:", pressure, "hPa")
    print("Wind Speed:", wind_speed, "m/s")
    print("============================================")

    sample_live_data = {
        'temperature_2m_max': temp_max,
        'temperature_2m_min': temp_min,
        'apparent_temperature_max': temp_max,
        'apparent_temperature_min': temp_min,
        'precipitation_sum': 0.0,
        'wind_speed_10m_max': wind_speed,
        'wind_gusts_10m_max': wind_speed,
        'wind_direction_10m_dominant': 0,
        'weather_code': 0
    }

    sample_live = pd.DataFrame([sample_live_data], columns=features)
    prediction = model.predict(sample_live)[0]
    rain_prediction = "Yes ☔" if prediction == 1 else "No 🌤"

    return {
        "city": city,
        "time": now,
        "temperature": temp,
        "temp_min": temp_min,
        "temp_max": temp_max,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "rain_prediction": rain_prediction
    }

# -----------------------------
# Test function when run directly
# -----------------------------
if __name__ == "__main__":
    result = get_live_weather_and_prediction()
    print("\n🌦 Will it rain tomorrow in", result["city"], "? -->", result["rain_prediction"])
