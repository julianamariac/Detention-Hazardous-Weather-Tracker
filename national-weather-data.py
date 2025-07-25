#!/usr/bin/env python3
# consolidated_weather_collector.py
# Collects weather data for ALL locations and saves in ONE consolidated file

import requests
import datetime
import json
import os
import sys
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Import our station configuration
from configuration import get_station_config, get_working_station, get_alerts_url, get_all_locations

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
DRIVE_FOLDER_ID = 'Find the characters for the google drive you woluld like to save data into https://drive.google.com/drive/folders/THESE CHARACTERS'

def authenticate_google_drive():
    """Authenticate and return Google Drive service object"""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080, open_browser=True)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def upload_to_google_drive(service, file_path, folder_id):
    """Upload file to specified Google Drive folder"""
    try:
        filename = os.path.basename(file_path)
        
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(file_path, mimetype='application/json')
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        print(f" Consolidated report uploaded: {filename}")
        return file.get('id')
        
    except Exception as e:
        print(f" Error uploading to Google Drive: {e}")
        return None

def collect_weather_data(location_code):
    """Collect weather data for a specific location with polite delays"""
    print(f" Collecting: {location_code}")
    
    # Get station configuration
    config = get_station_config(location_code)
    if not config:
        return {
            "location_code": location_code,
            "status": "ERROR",
            "error_message": "No configuration found",
            "collection_timestamp": datetime.datetime.now().isoformat()
        }
    
    # Find working weather station
    station_id, is_backup, status_message = get_working_station(location_code)
    
    if not station_id:
        # All stations down - create NA record
        return {
            "location_code": location_code,
            "location_name": config['location_name'],
            "region": config['region'],
            "status": "STATIONS_UNAVAILABLE",
            "error_message": status_message,
            "collection_timestamp": datetime.datetime.now().isoformat(),
            "temperature_C": None,
            "temperature_F": None,
            "relative_humidity": None,
            "wind_speed_kph": None,
            "wind_speed_mph": None,
            "text_description": "NA - Stations in Region of Interest Unavailable",
            "barometric_pressure": None,
            "visibility": None,
            "alerts": ["Unable to retrieve - stations unavailable"],
            "alert_count": 0,
            "alerts_gps": config['alerts_gps']
        }
    
    # Polite delay between API calls
    time.sleep(2)
    
    # Get weather observation
    try:
        url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
        response = requests.get(url, timeout=15)
        data = response.json()
        props = data.get('properties', {})
    except Exception as e:
        return {
            "location_code": location_code,
            "location_name": config['location_name'],
            "region": config['region'],
            "status": "API_ERROR",
            "error_message": f"Failed to get weather data: {str(e)}",
            "collection_timestamp": datetime.datetime.now().isoformat()
        }
    
    # Create comprehensive record
    current_time = datetime.datetime.now()
    record = {
        "collection_timestamp": current_time.isoformat(),
        "collection_date": current_time.strftime("%Y-%m-%d"),
        "collection_time": current_time.strftime("%H:%M:%S"),
        "location_code": location_code,
        "location_name": config['location_name'],
        "region": config['region'],
        "station_id": station_id,
        "is_backup_station": is_backup,
        "station_status": "BACKUP" if is_backup else "PRIMARY",
        "status": "SUCCESS",
        "nws_timestamp": props.get('timestamp'),
        "temperature_C": props.get('temperature', {}).get('value'),
        "temperature_F": None,
        "relative_humidity": props.get('relativeHumidity', {}).get('value'),
        "wind_speed_kph": props.get('windSpeed', {}).get('value'),
        "wind_speed_mph": None,
        "text_description": props.get('textDescription'),
        "barometric_pressure": props.get('barometricPressure', {}).get('value'),
        "visibility": props.get('visibility', {}).get('value')
    }
    
    # Convert units
    if record["temperature_C"] is not None:
        record["temperature_F"] = round((record["temperature_C"] * 9/5) + 32, 1)
    
    if record["wind_speed_kph"] is not None:
        record["wind_speed_mph"] = round(record["wind_speed_kph"] * 0.621371, 1)
    
    # Polite delay before alerts API call
    time.sleep(2)
    
    # Get weather alerts
    alerts_url = get_alerts_url(location_code)
    try:
        alerts_resp = requests.get(alerts_url, timeout=15)
        alerts_data = alerts_resp.json()
        alerts = [alert.get("properties", {}).get("headline", "No details") 
                 for alert in alerts_data.get("features", [])]
    except Exception as e:
        alerts = [f"Error fetching alerts: {str(e)}"]
    
    record["alerts"] = alerts
    record["alert_count"] = len(alerts)
    record["alerts_gps"] = config['alerts_gps']
    
    return record

def create_consolidated_report(all_records):
    """Create a consolidated report with summary statistics"""
    current_time = datetime.datetime.now()
    
    # Calculate summary statistics
    successful_collections = [r for r in all_records if r.get('status') == 'SUCCESS']
    failed_collections = [r for r in all_records if r.get('status') != 'SUCCESS']
    
    total_alerts = sum(r.get('alert_count', 0) for r in successful_collections)
    
    report = {
        "report_metadata": {
            "collection_timestamp": current_time.isoformat(),
            "collection_date": current_time.strftime("%Y-%m-%d"),
            "collection_time": current_time.strftime("%H:%M:%S"),
            "total_locations": len(all_records),
            "successful_collections": len(successful_collections),
            "failed_collections": len(failed_collections),
            "total_active_alerts": total_alerts,
            "collection_summary": "Consolidated weather report for all detention centers"
        },
        "location_data": all_records,
        "summary_statistics": {
            "locations_with_alerts": len([r for r in successful_collections if r.get('alert_count', 0) > 0]),
            "backup_stations_used": len([r for r in successful_collections if r.get('is_backup_station', False)]),
            "unavailable_regions": list(set(r.get('region', 'Unknown') for r in failed_collections))
        }
    }
    
    return report

def save_consolidated_report(report):
    """Save consolidated report locally and to Google Drive"""
    # Create directories
    raw_dir = "../raw_weather_json"
    os.makedirs(raw_dir, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = report['report_metadata']['collection_timestamp'].replace(':', '-').replace('.', '-')
    filename = f"consolidated_weather_report_{timestamp}.json"
    local_path = os.path.join(raw_dir, filename)
    
    # Save individual report
    with open(local_path, "w") as f:
        json.dump(report, f, separators=(',', ':'))
    
    # Append to continuous log
    log_path = os.path.join(raw_dir, "consolidated_weather_log.json")
    with open(log_path, "a") as f:
        json.dump(report, f, separators=(',', ':'))
        f.write("\n")
    
    # Upload to Google Drive
    try:
        drive_service = authenticate_google_drive()
        upload_to_google_drive(drive_service, local_path, DRIVE_FOLDER_ID)
    except Exception as e:
        print(f" Google Drive upload failed: {e}")
        print(" Data saved locally as backup")
    
    return local_path

def print_collection_summary(report):
    """Print summary of collection results"""
    metadata = report['report_metadata']
    stats = report['summary_statistics']
    
    print(f"\n COLLECTION SUMMARY - {metadata['collection_time']}")
    print(f" Successful: {metadata['successful_collections']}/{metadata['total_locations']} locations")
    print(f" Failed: {metadata['failed_collections']} locations")
    print(f" Total Active Alerts: {metadata['total_active_alerts']}")
    print(f" Backup Stations Used: {stats['backup_stations_used']}")
    
    if stats['unavailable_regions']:
        print(f" Unavailable Regions: {', '.join(stats['unavailable_regions'])}")
    
    # Show locations with issues
    failed_locations = [r for r in report['location_data'] if r.get('status') != 'SUCCESS']
    if failed_locations:
        print(f"\n FAILED LOCATIONS:")
        for location in failed_locations:
            print(f"   • {location.get('location_name', location.get('location_code'))}: {location.get('error_message', 'Unknown error')}")
    
    # Show locations with alerts
    locations_with_alerts = [r for r in report['location_data'] if r.get('alert_count', 0) > 0]
    if locations_with_alerts:
        print(f"\n LOCATIONS WITH ACTIVE ALERTS:")
        for location in locations_with_alerts:
            print(f"   • {location['location_name']}: {location['alert_count']} alert(s)")

def main():
    """Main function - collect data for all locations and create consolidated report"""
    print(f" Starting consolidated weather collection...")
    print(f" Using polite delays between API calls...")
    
    locations = get_all_locations()
    all_records = []
    
    start_time = time.time()
    
    for i, location_code in enumerate(locations, 1):
        print(f"[{i}/{len(locations)}] ", end="")
        try:
            record = collect_weather_data(location_code)
            all_records.append(record)
            
            # Status indicator
            if record.get('status') == 'SUCCESS':
            elif 'UNAVAILABLE' in record.get('status', ''):
            else:
                status_icon = "Cannot access record"
            
            print(f"{status_icon} {record.get('location_name', location_code)}")
            
        except Exception as e:
            print(f" {location_code}: Unexpected error - {str(e)}")
            all_records.append({
                "location_code": location_code,
                "status": "SYSTEM_ERROR",
                "error_message": str(e),
                "collection_timestamp": datetime.datetime.now().isoformat()
            })
    
    # Create and save consolidated report
    print(f"\nCreating consolidated report...")
    report = create_consolidated_report(all_records)
    saved_path = save_consolidated_report(report)
    
    # Print summary
    print_collection_summary(report)
    
    elapsed_time = time.time() - start_time
    print(f"\n Collection complete! ({elapsed_time:.1f} seconds)")
    print(f"Report saved: {saved_path}")

if __name__ == "__main__":
    main()
