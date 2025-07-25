#!/usr/bin/env python3
# station_finder.py
# Tool to find nearest weather stations for given GPS coordinates

import requests
import json
import math
import time

def get_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS points in miles"""
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 3956  # Radius of earth in miles
    return c * r

def find_nearest_stations(lat, lon, max_search_radius=200):
    """Find the 3 closest weather stations to given coordinates"""
    print(f"Finding stations near {lat}, {lon}")
    
    # Get stations from NWS API - use larger search area to ensure we find enough stations
    stations_url = f"https://api.weather.gov/stations?limit=500"
    
    try:
        response = requests.get(stations_url, timeout=15)
        if response.status_code != 200:
            print(f"Error getting stations: {response.status_code}")
            return []
        
        stations_data = response.json()
        stations = stations_data.get('features', [])
        
        # Calculate distances for all stations
        all_stations_with_distance = []
        
        for station in stations:
            try:
                props = station['properties']
                geometry = station['geometry']
                
                if geometry['type'] != 'Point':
                    continue
                
                station_lon, station_lat = geometry['coordinates']
                distance = get_distance(lat, lon, station_lat, station_lon)
                
                # Only consider stations within reasonable range
                if distance <= max_search_radius:
                    station_id = props.get('stationIdentifier', '').replace('https://api.weather.gov/stations/', '')
                    
                    station_info = {
                        'id': station_id,
                        'name': props.get('name', 'Unknown'),
                        'distance': round(distance, 1),
                        'lat': station_lat,
                        'lon': station_lon,
                        'elevation': props.get('elevation', {}).get('value')
                    }
                    
                    all_stations_with_distance.append(station_info)
                    
            except Exception as e:
                continue
        
        # Sort by distance and return the closest 3
        all_stations_with_distance.sort(key=lambda x: x['distance'])
        return all_stations_with_distance[:3]
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def test_station_data(station_id):
    """Test if a station has recent data"""
    try:
        url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            props = data.get('properties', {})
            if props.get('timestamp'):
                return True, "Has recent data"
        
        return False, "No recent data"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def find_stations_for_location(name, lat, lon):
    """Find and test the 3 closest stations for a specific location"""
    print(f"\n{name}")
    print(f"GPS: {lat}, {lon}")
    print("-" * 50)
    
    # Get the 3 closest stations
    stations = find_nearest_stations(lat, lon)
    
    if not stations:
        print("No nearby stations found")
        return []
    
    working_stations = []
    
    print(f"Found {len(stations)} closest stations:")
    
    for i, station in enumerate(stations):
        print(f"Testing station {i+1}/3: {station['id']} ({station['distance']} mi)... ", end="")
        
        # Add delay to be respectful to the API
        time.sleep(2)
        
        has_data, status = test_station_data(station['id'])
        print(status)
        
        if has_data:
            working_stations.append(station['id'])
    
    print(f"\nWorking stations for {name}:")
    for i, station_id in enumerate(working_stations):
        station_info = next(s for s in stations if s['id'] == station_id)
        if i == 0:
            role = "Primary"
        elif i == 1:
            role = "First Backup"
        else:
            role = "Second Backup"
        print(f"   {role}: {station_id} ({station_info['distance']} mi)")
    
    # Always return all 3 station IDs, even if some don't have data
    # This ensures we have backups configured
    all_station_ids = [station['id'] for station in stations]
    return all_station_ids

def generate_config_entry(name, lat, lon, stations, region="Unknown"):
    """Generate configuration code for a single location"""
    location_code = name.lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace(',', '')
    
    primary = stations[0] if len(stations) > 0 else None
    backup1 = stations[1] if len(stations) > 1 else None
    backup2 = stations[2] if len(stations) > 2 else None
    
    backups = [s for s in [backup1, backup2] if s is not None]
    
    config_text = f'    "{location_code}": {{\n'
    config_text += f'        "location_name": "{name}",\n'
    config_text += f'        "primary_station": "{primary}",\n'
    config_text += f'        "backup_stations": {backups},\n'
    config_text += f'        "alerts_gps": {{"lat": {lat}, "lon": {lon}}},\n'
    config_text += f'        "region": "{region}"\n'
    config_text += f'    }},'
    
    return config_text, location_code

def interactive_mode():
    """Interactive mode for finding stations for custom locations"""
    print("INTERACTIVE MODE: Find stations for custom locations")
    print("=" * 60)
    
    all_configs = []
    
    while True:
        print("\nEnter location details (or 'done' to finish):")
        
        # Get location name
        name = input("Location name: ").strip()
        if name.lower() == 'done':
            break
        
        if not name:
            print("Please enter a location name.")
            continue
        
        # Get coordinates
        try:
            lat_input = input("Latitude (e.g., 25.7617): ").strip()
            lon_input = input("Longitude (e.g., -80.1918): ").strip()
            
            lat = float(lat_input)
            lon = float(lon_input)
            
            # Basic validation
            if not (-90 <= lat <= 90):
                print("Latitude must be between -90 and 90")
                continue
            if not (-180 <= lon <= 180):
                print("Longitude must be between -180 and 180")
                continue
                
        except ValueError:
            print("Please enter valid numbers for coordinates.")
            continue
        
        # Get region (optional)
        region = input("Region/State (optional, e.g., 'Florida'): ").strip()
        if not region:
            region = "Unknown"
        
        # Find stations
        try:
            stations = find_stations_for_location(name, lat, lon)
            if stations:
                config_text, location_code = generate_config_entry(name, lat, lon, stations, region)
                all_configs.append((config_text, location_code, name))
                print(f"\nConfiguration generated for {name}")
            else:
                print(f"No stations found for {name}")
        except Exception as e:
            print(f"Error processing {name}: {e}")
        
        print("\n" + "="*60)
    
    return all_configs

def batch_mode():
    """Process predefined detention center locations"""
    # Default detention center locations
    LOCATIONS = [
        ("Alligator Detention Center", 25.86, -80.89, "Florida"),
        ("Baker County Detention Center", 30.29, -82.12, "Florida"),
        ("Broward Detention Center", 26.25, -80.15, "Florida"),
        ("Palm Beach Detention Center", 26.68, -80.10, "Florida"),
        ("Glades Detention Center", 26.84, -81.12, "Florida"),
        ("Krome Detention Center", 25.75, -80.49, "Florida"),
        ("Camp Blanding Detention Center", 29.98, -81.98, "Florida"),
        ("FTC Miami Detention Center", 25.78, -80.19, "Florida"),
    ]
    
    print("BATCH MODE: Processing predefined detention centers")
    print("=" * 60)
    
    all_configs = []
    
    for name, lat, lon, region in LOCATIONS:
        try:
            stations = find_stations_for_location(name, lat, lon)
            if stations:
                config_text, location_code = generate_config_entry(name, lat, lon, stations, region)
                all_configs.append((config_text, location_code, name))
        except Exception as e:
            print(f"Error processing {name}: {e}")
        
        print("\n" + "="*60)
    
    return all_configs

def main():
    """Main function - choose between interactive and batch mode"""
    print("Weather Station Finder for Detention Centers")
    print("=" * 60)
    print("\nChoose mode:")
    print("1. Interactive mode - Add your own locations with GPS coordinates")
    print("2. Batch mode - Process predefined detention centers")
    print("3. Single location lookup")
    
    while True:
        choice = input("\nEnter choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            all_configs = interactive_mode()
            break
        elif choice == "2":
            all_configs = batch_mode()
            break
        elif choice == "3":
            # Single location lookup
            print("\nSingle Location Lookup")
            print("-" * 30)
            
            name = input("Location name: ").strip()
            if not name:
                print("Please enter a location name.")
                return
            
            try:
                lat = float(input("Latitude: ").strip())
                lon = float(input("Longitude: ").strip())
                region = input("Region (optional): ").strip() or "Unknown"
                
                stations = find_stations_for_location(name, lat, lon)
                if stations:
                    config_text, location_code = generate_config_entry(name, lat, lon, stations, region)
                    all_configs = [(config_text, location_code, name)]
                else:
                    print("No stations found.")
                    return
                    
            except ValueError:
                print("Please enter valid coordinates.")
                return
            break
        else:
            print("Please enter 1, 2, or 3.")
    
    # Output results
    if all_configs:
        print("\n" + "="*60)
        print("CONFIGURATION CODE:")
        print("-" * 30)
        print("Copy this code into your configuration.py file:")
        print()
        
        for config_text, location_code, name in all_configs:
            print(config_text)
        
        print("\nLocation codes for weather_tracker_gdrive.py:")
        print("-" * 50)
        for config_text, location_code, name in all_configs:
            print(f"'{location_code}' - {name}")
        
        print("\n" + "="*60)
        print("Next steps:")
        print("1. Copy the configuration code above into your configuration.py file")
        print("2. Update the STATION_CONFIG dictionary in configuration.py")
        print("3. Run weather_tracker_gdrive.py to collect data")
        print()
        print("IMPORTANT: Wait at least 1 hour between data collection runs")
        print("to avoid overloading the National Weather Service API.")
    else:
        print("No configurations generated.")

if __name__ == "__main__":
    main()
