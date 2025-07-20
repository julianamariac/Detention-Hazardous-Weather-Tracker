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
    "wind_speed_kph": props.get('windSpeed', {}).get('value'),
    "text_description": props.get('textDescription')
}

# Step 4: Get weather alerts for your location
try:
    alerts_url = "https://api.weather.gov/alerts/active?point=25.76,-80.19"
    alerts_resp = requests.get(alerts_url)
    alerts_data = alerts_resp.json()
    alerts = [alert.get("properties", {}).get("headline", "No details") for alert in    alerts_data.get("features", [])]
except:
     alerts = ["Error fetching alerts"]
# Add alerts to the record
record["alerts"] = alerts
record["alert_count"] = len(alerts)

# Step 5: Save as audit log (append to file or send to Google Sheet)
with open("weather_audit_log.json", "a") as f:
    json.dump(record, f)
    f.write("\n")

print("Logged weather:", record)

# Optional: Print alerts separately for visibility
if alerts:
    print(f"\n  {len(alerts)} Active Alert(s):")
    for i, alert in enumerate(alerts, 1):
        print(f"  {i}. {alert}")
else:
    print("\n No active weather alerts")
