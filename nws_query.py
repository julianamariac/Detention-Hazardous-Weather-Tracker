import requests
import datetime
import json

# Step 1: Set station ID (use KMIA or any near your GPS)
station_id = "KMIA"

# Step 2: Get latest observation
url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
response = requests.get(url)
data = response.json()

# Step 3: Extract key info
props = data.get('properties', {})
record = {
    "timestamp": props.get('timestamp'),
    "temperature_C": props.get('temperature', {}).get('value'),
    "relative_humidity": props.get('relativeHumidity', {}).get('value'),
    "precip_last_24hour_mm": props.get('precipitationLast24Hours', {}).get('value'),
    "wind_speed_kph": props.get('windSpeed', {}).get('value'),
    "text_description": props.get('textDescription')
}

# Step 4: Save as audit log (append to file or send to Google Sheet)
with open("weather_audit_log.json", "a") as f:
    json.dump(record, f)
    f.write("\n")

print("Logged weather:", record)
