# Detention Center Weather Tracking System - Setup Guide

This guide helps you set up an automated weather tracking system for detention centers. The system collects weather data and alerts from the National Weather Service and saves them to Google Drive for monitoring conditions at detention facilities.

## Important Usage Guidelines

**PLEASE READ**: This system uses the National Weather Service's free public API. To be respectful of this public service:
- **Only run data collection ONCE PER HOUR maximum**
- The system includes built-in delays between API calls
- Do not modify the delay timings in the code

## What You'll Need

- A Windows or Mac computer with internet connection
- About 1-2 hours for initial setup
- A Google account (free)
- Basic comfort with running commands in a terminal

## Part 1: Setting Up Google Drive and Google Cloud (Free)

### Step 1: Create Google Drive Folder

1. Go to [Google Drive](https://drive.google.com) and sign in
2. Click "New" → "Folder"
3. Name it "Detention Weather Data"
4. Open the folder and copy the folder ID from the URL:
   - The URL will look like: `https://drive.google.com/drive/folders/1ABC123XYZ456`
   - The folder ID is the part after `/folders/`: `1ABC123XYZ456`
   - Save this ID - you'll need it later

### Step 2: Set Up Google Cloud Project (FREE)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name your project "Weather Tracker" and click "Create"
4. Wait for the project to be created (takes ~1 minute)

### Step 3: Enable Google Drive API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. Click on "Google Drive API" and click "Enable"
4. Wait for it to enable (takes ~30 seconds)

### Step 4: Create Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, click "Configure Consent Screen":
   - Choose "External" and click "Create"
   - Fill in required fields:
     - App name: "Weather Tracker"
     - User support email: (your email)
     - Developer contact: (your email)
   - Click "Save and Continue" through all steps
4. Back in Credentials, click "Create Credentials" → "OAuth client ID"
5. Choose "Desktop application"
6. Name it "Weather Tracker Client"
7. Click "Create"
8. Download the JSON file - rename it to `credentials.json`

### Cost Breakdown (It's Free!)

- Google Drive: 15GB free storage (our data uses ~1MB per month)
- Google Cloud: Free tier includes 100 API calls per day (we make ~25 per day)
- **Total monthly cost: $0.00**

The system will stay free as long as you:
- Don't exceed 15GB in Google Drive (our data is tiny)
- Don't make more than 100 API calls per day (follow the 1-hour rule)

## Part 2: Installing Python and Dependencies

### For Windows Users:

1. **Install Python:**
   - Go to [python.org](https://python.org/downloads/)
   - Download Python 3.11 or newer
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Click "Install Now"

2. **Test Python Installation:**
   - Press `Windows + R`, type `cmd`, press Enter
   - Type `python --version` and press Enter
   - You should see something like "Python 3.11.x"

3. **Install Required Packages:**
   ```
   pip install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

### For Mac Users:

1. **Install Python:**
   - Go to [python.org](https://python.org/downloads/)
   - Download Python 3.11 or newer for macOS
   - Install the downloaded package

2. **Test Python Installation:**
   - Press `Command + Space`, type "Terminal", press Enter
   - Type `python3 --version` and press Enter
   - You should see something like "Python 3.11.x"

3. **Install Required Packages:**
   ```
   pip3 install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

## Part 3: Finding GPS Coordinates for Your Locations

### How to Find GPS Coordinates

Before setting up the tracker, you need GPS coordinates for the detention centers you want to monitor:

1. **Open Google Maps** in your web browser
2. **Search for the detention center** by name or address
3. **Right-click directly on the detention center location** on the map
4. **Select "What's here?"** from the menu
5. **Copy the coordinates** that appear (they look like: 25.7617, -80.1918)
   - The first number is latitude
   - The second number is longitude
   - You need both numbers

### Example Coordinate Lookup:
- Search: "Krome Detention Center, Miami"
- Right-click on the facility
- Coordinates shown: 25.7500, -80.4900
- Latitude: 25.7500
- Longitude: -80.4900

## Part 4: Setting Up the Weather Tracker

### Step 1: Create Directory Structure

Create this exact folder structure on your computer:

```
weather-tracker/
├── credentials.json          (from Google Cloud setup)
├── station_finder.py         (downloaded from GitHub)
├── weather_tracker_gdrive.py (downloaded from GitHub)
├── configuration.py          (you'll create this)
└── raw_weather_json/         (created automatically)
    ├── consolidated_weather_report_[timestamp].json
    └── consolidated_weather_log.json
```

### Step 2: Download the Code

1. Download all the Python files from the GitHub repository
2. Create a new folder on your computer called "weather-tracker"
3. Put all the downloaded files in this folder
4. Put your `credentials.json` file (from Google Cloud setup) in the same folder

### Step 3: Find Weather Stations for Your Locations

Now you need to find the closest weather stations for each detention center:

1. **Run the station finder** in your weather-tracker folder:
   - Windows: Open Command Prompt, navigate to folder, run `python station_finder.py`
   - Mac: Open Terminal, navigate to folder, run `python3 station_finder.py`

2. **Choose your mode:**
   - **Option 1 - Interactive Mode**: Add your own locations one by one
   - **Option 2 - Batch Mode**: Use predefined Florida detention centers
   - **Option 3 - Single Location**: Look up one location quickly

3. **For Interactive Mode** (most common):
   - Enter location name: "Example Detention Center"
   - Enter latitude: 25.7500
   - Enter longitude: -80.4900
   - Enter region: "Florida"
   - Repeat for each location you want to monitor

4. **Copy the configuration code** that the program outputs
5. **Create a new file** called `configuration.py` in your weather-tracker folder
6. **Paste the configuration code** into this file

### Important Notes About Station Finding:
- The program tests each weather station to make sure it has recent data
- It finds the 3 closest stations (1 primary, 2 backups)
- You only need to run this once when setting up new locations
- The process takes 2-3 minutes per location due to respectful API delays

### Step 4: Configure Google Drive Folder

1. Open `weather_tracker_gdrive.py` in a text editor (Notepad on Windows, TextEdit on Mac)
2. Find this line near the top:
   ```python
   DRIVE_FOLDER_ID = 'Find the characters for the google drive you woluld like to save data into https://drive.google.com/drive/folders/THESE CHARACTERS'
   ```
3. Replace the entire text between the quotes with your Google Drive folder ID from Step 1
4. It should look like:
   ```python
   DRIVE_FOLDER_ID = '1ABC123XYZ456'
   ```
5. Save the file

### Step 5: Create Complete Configuration File

After running the station finder, you need to create a complete `configuration.py` file. Here's the template:

```python
# Configuration for detention center weather stations

# Paste your station configuration from station_finder.py here
STATION_CONFIG = {
    # Example entry - replace with your actual locations:
    "example_detention_center": {
        "location_name": "Example Detention Center",
        "primary_station": "KMIA",
        "backup_stations": ["KFXE", "KOPF"],
        "alerts_gps": {"lat": 25.7500, "lon": -80.4900},
        "region": "Florida"
    },
    # Add more locations here...
}

def get_station_config(location_code):
    """Get configuration for a location"""
    return STATION_CONFIG.get(location_code)

def get_working_station(location_code):
    """Get working weather station for location with fallback logic"""
    import requests
    
    config = get_station_config(location_code)
    if not config:
        return None, False, "No configuration found"
    
    # Try primary station first
    primary = config['primary_station']
    if test_station_active(primary):
        return primary, False, "Using primary station"
    
    # Try backup stations
    for backup in config.get('backup_stations', []):
        if test_station_active(backup):
            return backup, True, f"Using backup station {backup}"
    
    return None, False, "All stations unavailable"

def test_station_active(station_id):
    """Test if a station has recent data"""
    try:
        url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            props = data.get('properties', {})
            return props.get('timestamp') is not None
        return False
    except:
        return False

def get_alerts_url(location_code):
    """Get weather alerts URL for location"""
    config = get_station_config(location_code)
    if not config:
        return None
    
    gps = config['alerts_gps']
    return f"https://api.weather.gov/alerts/active?point={gps['lat']},{gps['lon']}"

def get_all_locations():
    """Get list of all location codes"""
    return list(STATION_CONFIG.keys())
```

### Step 6: First Run and Authentication

1. Open your terminal/command prompt in the weather-tracker folder
2. Run the weather tracker:
   - Windows: `python weather_tracker_gdrive.py`
   - Mac: `python3 weather_tracker_gdrive.py`

3. The first time you run it:
   - A browser window will open
   - Sign in to your Google account
   - Click "Allow" to give the app permission to access Drive
   - You'll see "The authentication flow has completed" - close the browser

4. The script will now collect weather data and upload it to Google Drive

### Step 2: Verify It's Working

1. Check your Google Drive folder - you should see new JSON files
2. The console should show collection progress without errors
3. Each run should take about 2-3 minutes to complete

## Part 5: Running the System

### Complete Workflow Summary

Here's how the entire system works:

1. **One-time setup**: Find GPS coordinates for detention centers
2. **One-time setup**: Run `station_finder.py` to find weather stations
3. **One-time setup**: Create `configuration.py` with station assignments
4. **Regular use**: Run `weather_tracker_gdrive.py` to collect data (max once per hour)

### Manual Collection

Run the weather collection manually when you want data:

**Windows:**
```
cd path\to\your\weather-tracker
python weather_tracker_gdrive.py
```

**Mac/Linux:**
```
cd /path/to/your/weather-tracker
python3 weather_tracker_gdrive.py
```

### Automated Scheduling (Optional)

For continuous monitoring, you can schedule the script to run automatically. **Remember: Never schedule more frequently than once per hour.**

#### Windows - Task Scheduler

1. **Open Task Scheduler:**
   - Press `Windows + R`, type `taskschd.msc`, press Enter

2. **Create Basic Task:**
   - Click "Create Basic Task" in the right panel
   - Name: "Weather Tracker"
   - Description: "Detention center weather monitoring"
   - Click "Next"

3. **Set Trigger:**
   - Choose "Daily"
   - Set start time (e.g., 8:00 AM)
   - Recur every: 1 days
   - Click "Next"

4. **Set Action:**
   - Choose "Start a program"
   - Program/script: `python`
   - Add arguments: `weather_tracker_gdrive.py`
   - Start in: `C:\path\to\your\weather-tracker` (your actual folder path)
   - Click "Next"

5. **Advanced Settings:**
   - Check "Open the Properties dialog"
   - Click "Finish"

6. **In Properties Dialog:**
   - Go to "Triggers" tab → Edit → "Advanced settings"
   - Check "Repeat task every:" 
   - Set to "1 hour"
   - Set duration to "Indefinitely"
   - Click "OK"

#### Mac - Cron (Terminal Method)

1. **Open Terminal**

2. **Edit crontab:**
   ```bash
   crontab -e
   ```

3. **Add this line** (replace `/path/to/your/weather-tracker` with actual path):
   ```bash
   0 * * * * cd /path/to/your/weather-tracker && /usr/bin/python3 weather_tracker_gdrive.py >> /path/to/your/weather-tracker/cron.log 2>&1
   ```

4. **Save and exit** (in nano: Ctrl+X, then Y, then Enter)

#### Mac - Automator (GUI Method)

1. **Open Automator** (Applications → Automator)

2. **Create New Document:**
   - Choose "Calendar Alarm"

3. **Add Actions:**
   - Search for "Run Shell Script"
   - Drag it to the workflow area
   - Change "Pass input" to "as arguments"
   - Enter this script:
   ```bash
   cd /path/to/your/weather-tracker
   /usr/bin/python3 weather_tracker_gdrive.py
   ```

4. **Save the workflow**

5. **Set up Calendar Event:**
   - Open Calendar app
   - Create new event: "Weather Collection"
   - Set to repeat every hour
   - Add the Automator workflow as an alarm

#### Linux - Cron

1. **Open terminal**

2. **Edit crontab:**
   ```bash
   crontab -e
   ```

3. **Add hourly collection** (replace path):
   ```bash
   0 * * * * cd /path/to/your/weather-tracker && /usr/bin/python3 weather_tracker_gdrive.py >> /path/to/your/weather-tracker/cron.log 2>&1
   ```

4. **For specific times only** (e.g., every 3 hours from 6 AM to 9 PM):
   ```bash
   0 6,9,12,15,18,21 * * * cd /path/to/your/weather-tracker && /usr/bin/python3 weather_tracker_gdrive.py >> /path/to/your/weather-tracker/cron.log 2>&1
   ```

5. **Save and exit**

#### Ubuntu/Debian - Systemd Timer (Advanced)

For more reliable service management:

1. **Create service file:**
   ```bash
   sudo nano /etc/systemd/system/weather-tracker.service
   ```

2. **Add content** (replace username and path):
   ```ini
   [Unit]
   Description=Detention Center Weather Tracker
   After=network.target

   [Service]
   Type=oneshot
   User=your-username
   WorkingDirectory=/path/to/your/weather-tracker
   ExecStart=/usr/bin/python3 weather_tracker_gdrive.py
   ```

3. **Create timer file:**
   ```bash
   sudo nano /etc/systemd/system/weather-tracker.timer
   ```

4. **Add timer content:**
   ```ini
   [Unit]
   Description=Run weather tracker every hour
   Requires=weather-tracker.service

   [Timer]
   OnCalendar=hourly
   Persistent=true

   [Install]
   WantedBy=timers.target
   ```

5. **Enable and start:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable weather-tracker.timer
   sudo systemctl start weather-tracker.timer
   ```

### Scheduling Best Practices

**Recommended Schedule Options:**

1. **Hourly Collection** (24 times per day):
   - Good for: Active monitoring during emergencies
   - Impact: Higher API usage but still within free limits

2. **Every 3 Hours** (8 times per day):
   - Good for: Regular monitoring with lower API usage
   - Times: 6 AM, 9 AM, 12 PM, 3 PM, 6 PM, 9 PM

3. **Twice Daily** (2 times per day):
   - Good for: Basic monitoring with minimal API usage
   - Times: 8 AM and 8 PM

4. **Business Hours Only**:
   - Good for: Office-based monitoring
   - Times: Every 2 hours from 8 AM to 6 PM

**Important Scheduling Notes:**
- Never schedule more than once per hour
- Consider time zones if monitoring multiple regions
- Monitor your Google Drive storage (though usage is minimal)
- Check logs regularly to ensure the system is working
- The system respects API rate limits with built-in delays

### Important Usage Rules

- **Wait at least 1 hour between runs**
- The system will collect data for all detention centers in one run
- Each file contains weather data and active alerts for all locations
- Data is saved both locally and to Google Drive

### Understanding File Structure

Your final directory should look like this:

```
weather-tracker/
├── credentials.json                    (Google API credentials)
├── token.json                         (Created after first auth)
├── station_finder.py                  (Finds weather stations)
├── weather_tracker_gdrive.py          (Main data collector)
├── configuration.py                   (Your station assignments)
└── raw_weather_json/                  (Output folder)
    ├── consolidated_weather_report_2025-07-24T10-30-15.json
    ├── consolidated_weather_report_2025-07-24T11-35-22.json
    └── consolidated_weather_log.json  (Continuous log)
```

### What the System Collects

- Temperature (Celsius and Fahrenheit)
- Humidity levels
- Wind speed
- Weather conditions description
- Barometric pressure
- Visibility
- Active weather alerts and warnings
- Station backup information

## Troubleshooting

### Common Issues:

**"Python is not recognized" (Windows):**
- Reinstall Python and make sure to check "Add Python to PATH"

**"pip is not recognized" (Windows):**
- Try `python -m pip install` instead of just `pip install`

**"Permission denied" errors:**
- Make sure you have write permissions in your folder
- Try running as administrator (Windows) or with sudo (Mac)

**"No module named..." errors:**
- Make sure all packages installed correctly
- Try reinstalling: `pip install --upgrade [package-name]`

**Google authentication not working:**
- Make sure `credentials.json` is in the same folder as the scripts
- Delete `token.json` and try authenticating again

**No weather data collected:**
- Check your internet connection
- Verify the National Weather Service API is working
- Make sure you waited at least 1 hour since last run

## Understanding the Output

The system creates two types of files:

1. **Individual reports**: `consolidated_weather_report_TIMESTAMP.json`
   - One complete snapshot of all locations
   - Includes summary statistics

2. **Continuous log**: `consolidated_weather_log.json`
   - Appends each collection run
   - Historical record of all collections

Each record includes:
- Collection timestamp
- Location details
- Weather measurements
- Active alerts
- Station status (primary/backup)
- Error information if collection failed

## Data Usage and Privacy

- This system only collects publicly available weather data
- No personal information is collected or stored
- All data comes from the National Weather Service public API
- Data is stored in your personal Google Drive account

## Getting Help

If you encounter issues:

1. Check that all files are in the same folder
2. Verify your Google Drive folder ID is correct
3. Make sure you're following the 1-hour minimum interval
4. Check that your internet connection is stable

This system helps monitor weather conditions at detention facilities to ensure transparency and accountability in detention conditions.

**Remember: Only run data collection once per hour maximum to respect the National Weather Service's public API.**
