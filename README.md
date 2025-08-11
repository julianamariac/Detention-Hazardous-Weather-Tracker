# Detention Center Weather Tracking System - Complete Setup Guide

This guide helps you set up an automated weather tracking and analysis system for detention centers. The system collects weather data from the National Weather Service, saves it to Google Drive, and automatically analyzes conditions for legal documentation and transparency.

## System Overview

This complete system has three main components:

1. **Data Collection**: Hourly weather monitoring from verified NWS stations
2. **Daily Analysis**: Cryptographically verified hazard detection and gap analysis
3. **Legal Reporting**: Court-ready documentation organized by detention center

## Important Usage Guidelines

**PLEASE READ**: This system uses the National Weather Service's free public API. To be respectful of this public service:
- **Only run data collection ONCE PER HOUR maximum**
- The system includes built-in delays between API calls
- Do not modify the delay timings in the code to decrease delay, but feel free to increase delay between pings

## What You'll Need

- A Windows or Mac computer with internet connection
- About 2-3 hours for initial setup
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
### For Linux Users:

#### Ubuntu/Debian Systems:

1. **Update package list:**
   ```bash
   sudo apt update
   ```

2. **Install Python and pip:**
   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```

3. **Test Python Installation:**
   - Open Terminal (Ctrl+Alt+T)
   - Type `python3 --version` and press Enter
   - You should see something like "Python 3.8.x" or newer

4. **Install Required Packages:**
   ```bash
   pip3 install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

#### RHEL/CentOS/Fedora Systems:

1. **For RHEL/CentOS 8+ or Fedora:**
   ```bash
   sudo dnf install python3 python3-pip
   ```

2. **For older RHEL/CentOS 7:**
   ```bash
   sudo yum install python3 python3-pip
   ```

3. **Test Python Installation:**
   ```bash
   python3 --version
   ```

4. **Install Required Packages:**
   ```bash
   pip3 install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

#### Arch Linux:

1. **Install Python:**
   ```bash
   sudo pacman -S python python-pip
   ```

2. **Test Python Installation:**
   ```bash
   python --version
   ```

3. **Install Required Packages:**
   ```bash
   pip install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

#### If pip install fails with permissions:

Some Linux distributions require using `--user` flag:
```bash
pip3 install --user requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

Or create a virtual environment (recommended):
```bash
python3 -m venv weather-tracker-env
source weather-tracker-env/bin/activate
pip install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

If using a virtual environment, remember to activate it each time:
```bash
source weather-tracker-env/bin/activate
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

## Part 4: Setting Up the Complete Weather System

### Step 1: Create Directory Structure

Create this exact folder structure on your computer:

```
weather-tracker/
├── Scripts/                           (Main scripts folder)
│   ├── credentials.json               (from Google Cloud setup)
│   ├── token.json                     (created after first auth)
│   ├── station_finder.py              (finds weather stations)
│   ├── weather_tracker_gdrive.py      (collects hourly data)
│   ├── configuration.py               (station assignments)
│   ├── verifiable_weather_analyzer.py (daily analysis)
│   ├── enhanced_weather_analyzer.py   (center-focused reports)
│   └── bulk_uploader.py               (upload utility)
├── raw_weather_json/                  (hourly data storage)
│   ├── consolidated_weather_report_[timestamp].json
│   └── consolidated_weather_log.json
├── daily_analysis/                    (daily analysis output)
│   ├── daily_analysis_[date].json
│   └── enhanced_analysis_[date].json
├── daily_verification/                (verification records)
│   ├── verification_summary_[date].json
│   └── public_verification_log.json
└── center_reports/                    (center-focused reports)
    ├── center_analysis_[date].json
    └── center_report_[date].txt
```

### Step 2: Download the Code

1. Download all the Python files from the GitHub repository
2. Create a new folder on your computer called "weather-tracker"
3. Create a "Scripts" subfolder inside "weather-tracker"
4. Put all the downloaded Python files in the "Scripts" folder
5. Put your `credentials.json` file (from Google Cloud setup) in the "Scripts" folder

### Step 3: Find Weather Stations for Your Locations

Now you need to find the closest weather stations for each detention center:

1. **Navigate to your Scripts folder** in terminal/command prompt
2. **Run the station finder**:
   - Windows: `python station_finder.py`
   - Mac: `python3 station_finder.py`

3. **The program will automatically find stations** for predefined Florida detention centers and output configuration code

4. **Copy the configuration code** that the program outputs
5. **Create a new file** called `configuration.py` in your Scripts folder
6. **Paste the configuration code** into this file

### Important Notes About Station Finding:
- The program tests each weather station to make sure it has recent data
- It finds 3-4 closest stations (1 primary, 2-3 backups) for each location
- You only need to run this once during setup
- The process takes 5-10 minutes due to respectful API delays

### Step 4: Configure Google Drive Folder

1. Open `weather_tracker_gdrive.py` in a text editor (Notepad on Windows, TextEdit on Mac)
2. Find this line near the top:
   ```python
   DRIVE_FOLDER_ID = '1p2sRZpUMu9OoGgeWr-ya8x7DSl7VO1lt'
   ```
3. Replace the text between the quotes with your Google Drive folder ID from Step 1
4. It should look like:
   ```python
   DRIVE_FOLDER_ID = '1ABC123XYZ456'
   ```
5. Save the file

### Step 5: First Run and Authentication

1. Open your terminal/command prompt in the Scripts folder
2. Run the weather tracker for the first time:
   - Windows: `python weather_tracker_gdrive.py`
   - Mac: `python3 weather_tracker_gdrive.py`

3. The first time you run it:
   - A browser window will open
   - Sign in to your Google account
   - Click "Allow" to give the app permission to access Drive
   - You'll see "The authentication flow has completed" - close the browser

4. The script will now collect weather data and upload it to Google Drive

### Step 6: Verify Data Collection is Working

1. Check your Google Drive folder - you should see new JSON files
2. The console should show collection progress without errors
3. Each run should take about 2-3 minutes to complete
4. Check that the `raw_weather_json` folder was created with data files

## Part 5: Setting Up Daily Analysis

The analysis system creates detailed reports about weather conditions at each detention center, including auditable documentation features.

### What the Analysis Does

1. **Enhanced Weather Analyzer**:
   - Organizes analysis by individual detention centers
   - Shows hazard timelines throughout each day
   - Creates human-readable reports for legal documentation

### Test the Analysis System

Before setting up automation, test both analyzers manually:

1. **Wait 24 hours after starting data collection** (so you have a full day of data)

2. **Run the verifiable analyzer**:
   - Windows: `python verifiable_weather_analyzer.py`
   - Mac: `python3 verifiable_weather_analyzer.py`
   
   This analyzes yesterday's data by default.

3. **Run the enhanced analyzer**:
   - Windows: `python enhanced_weather_analyzer.py`
   - Mac: `python3 enhanced_weather_analyzer.py`

4. **Check the output folders**:
   - `daily_analysis/` should contain analysis JSON files
   - `daily_verification/` should contain verification summaries
   - `center_reports/` should contain human-readable reports

### Understanding Analysis Output

The system will show you:
- **Data Quality**: How complete your daily data collection was
- **Missing Hours**: Any gaps in collection and likely causes
- **Hazard Detection**: Extreme heat, cold, humidity, storms, etc.
- **Risk Assessment**: Overall risk level for each day
- **Center Reports**: Individual analysis for each detention facility

## Part 6: Automated Scheduling

### Setting Up Hourly Data Collection

For continuous monitoring, schedule the data collection to run automatically. **Remember: Never schedule more frequently than once per hour.**

#### Windows - Task Scheduler

1. **Open Task Scheduler:**
   - Press `Windows + R`, type `taskschd.msc`, press Enter

2. **Create Basic Task:**
   - Click "Create Basic Task" in the right panel
   - Name: "Weather Data Collection"
   - Description: "Hourly detention center weather monitoring"
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
   - Start in: `C:\path\to\your\weather-tracker\Scripts` (your actual folder path)
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

#### Mac/Linux - Cron for Hourly Collection

1. **Open Terminal**

2. **Edit crontab:**
   ```bash
   crontab -e
   ```

3. **Add hourly collection** (replace `/path/to/your/weather-tracker/Scripts` with actual path):
   ```bash
   0 * * * * cd /path/to/your/weather-tracker/Scripts && /usr/bin/python3 weather_tracker_gdrive.py >> /path/to/your/weather-tracker/collection.log 2>&1
   ```

4. **Save and exit** (in nano: Ctrl+X, then Y, then Enter)

### Setting Up Daily Analysis

Schedule the analysis to run once per day at 12:05 AM to analyze the previous day's complete data (from 12:00 AM to 11:59 PM).

#### Windows - Task Scheduler for Daily Analysis

Create two separate tasks:

**Task 1: Verifiable Analysis**
1. Create Basic Task: "Daily Weather Analysis"
2. Set Trigger: Daily at 12:05 AM
3. Set Action:
   - Program/script: `python`
   - Arguments: `verifiable_weather_analyzer.py`
   - Start in: `C:\path\to\your\weather-tracker\Scripts`

**Task 2: Enhanced Analysis**
1. Create Basic Task: "Daily Enhanced Analysis"
2. Set Trigger: Daily at 12:10 AM
3. Set Action:
   - Program/script: `python`
   - Arguments: `enhanced_weather_analyzer.py`
   - Start in: `C:\path\to\your\weather-tracker\Scripts`

#### Mac/Linux - Cron for Daily Analysis

1. **Edit crontab:**
   ```bash
   crontab -e
   ```

2. **Add daily analysis** (replace path with your actual path):
   ```bash
   # Daily verifiable analysis at 12:05 AM
   5 0 * * * cd /path/to/your/weather-tracker/Scripts && /usr/bin/python3 verifiable_weather_analyzer.py >> /path/to/your/weather-tracker/analysis.log 2>&1
   
   # Daily enhanced analysis at 12:10 AM
   10 0 * * * cd /path/to/your/weather-tracker/Scripts && /usr/bin/python3 enhanced_weather_analyzer.py >> /path/to/your/weather-tracker/analysis.log 2>&1
   ```

3. **Save and exit**

### Complete Cron Schedule Example

Here's what your complete crontab should look like:

```bash
# Hourly weather data collection
0 * * * * cd /path/to/your/weather-tracker/Scripts && /usr/bin/python3 weather_tracker_gdrive.py >> /path/to/your/weather-tracker/collection.log 2>&1

# Daily analysis at 12:05 AM (analyzes previous day's data)
5 0 * * * cd /path/to/your/weather-tracker/Scripts && /usr/bin/python3 verifiable_weather_analyzer.py >> /path/to/your/weather-tracker/analysis.log 2>&1

# Daily enhanced analysis at 12:10 AM
10 0 * * * cd /path/to/your/weather-tracker/Scripts && /usr/bin/python3 enhanced_weather_analyzer.py >> /path/to/your/weather-tracker/analysis.log 2>&1
```

## Part 7: Understanding the Complete System

### Daily Workflow

Once fully set up, here's what happens automatically each day:

**Every Hour (24 times per day):**
- `weather_tracker_gdrive.py` collects current weather data
- Data saved locally and uploaded to Google Drive
- About 2-3 minutes per collection

**Every Day at 12:05 AM:**
- `verifiable_weather_analyzer.py` analyzes the previous day's data
- Creates cryptographically verified analysis reports
- Documents data quality and any missing collection periods

**Every Day at 12:10 AM:**
- `enhanced_weather_analyzer.py` creates center-focused reports
- Organizes hazards by individual detention centers
- Generates human-readable reports for legal documentation

### File Structure After Full Setup

```
weather-tracker/
├── Scripts/
│   ├── weather_tracker_gdrive.py      (runs hourly)
│   ├── verifiable_weather_analyzer.py (runs daily at 12:05 AM)
│   ├── enhanced_weather_analyzer.py   (runs daily at 12:10 AM)
│   ├── configuration.py               (station assignments)
│   ├── station_finder.py              (setup tool)
│   ├── bulk_uploader.py               (maintenance tool)
│   ├── credentials.json               (Google API credentials)
│   └── token.json                     (Google auth token)
├── raw_weather_json/                  (hourly collection output)
│   ├── consolidated_weather_report_2024-08-11T14-30-15.json
│   ├── consolidated_weather_report_2024-08-11T15-35-22.json
│   └── consolidated_weather_log.json  (continuous log)
├── daily_analysis/                    (verifiable analysis output)
│   ├── daily_analysis_2024-08-10.json
│   └── daily_analysis_2024-08-11.json
├── daily_verification/                (verification summaries)
│   ├── verification_summary_2024-08-10.json
│   ├── verification_summary_2024-08-11.json
│   └── public_verification_log.json
├── center_reports/                    (human-readable reports)
│   ├── center_analysis_2024-08-10.json
│   ├── center_report_2024-08-10.txt
│   ├── center_analysis_2024-08-11.json
│   └── center_report_2024-08-11.txt
├── collection.log                     (collection activity log)
└── analysis.log                       (analysis activity log)
```

### What the System Monitors

**Current Detention Centers (Florida):**
- Miami Dade Detention Center (Alligator)
- Baker County Detention Center
- Broward County Detention Center
- Palm Beach County Detention Center
- Glades Detention Center
- Krome Detention Center
- Camp Blanding Detention Center
- FTC Miami Detention Center

**Weather Data Collected:**
- Temperature (Celsius and Fahrenheit)
- Relative humidity
- Wind speed (kilometers/hour and miles/hour)
- Barometric pressure
- Visibility
- Weather condition descriptions
- Active weather alerts and warnings

**Hazard Detection Thresholds:**
- Extreme Heat: 95°F (35°C)
- Extreme Cold: 32°F (0°C) - freezing conditions
- High Humidity: 85% (dangerous in crowded facilities)
- Dangerous Winds: 39 mph (tropical storm force)
- Low Visibility: Less than 1 mile
- Extreme Pressure: Below 29.00 or above 31.00 inches Hg
- Weather Alerts: Tornado, hurricane, flood, severe thunderstorm warnings

## Part 8: Legal Documentation Features

### Cryptographic Verification

All analysis reports include:
- **Code Verification**: SHA-256 hash of the analysis code
- **Data Verification**: SHA-256 hash of input and output data
- **Threshold Documentation**: Hardcoded detection thresholds
- **Methodology**: Transparent, reproducible analysis steps

### Data Quality Documentation

Every daily report includes:
- **Collection Completeness**: Percentage of expected hourly reports collected
- **Missing Data Periods**: Specific hours with no data and likely causes
- **Data Quality Rating**: Excellent, Good, Fair, Poor, or Insufficient
- **Reliability Assessment**: Legal documentation of analysis reliability

### Chain of Custody

- All data sourced from official National Weather Service API
- No data manipulation or selective reporting
- Missing periods documented with explanations
- Open-source code for full transparency

## Troubleshooting

### Common Issues:

**"Python is not recognized" (Windows):**
- Reinstall Python and make sure to check "Add Python to PATH"

**"pip is not recognized" (Windows):**
- Try `python -m pip install` instead of just `pip install`

**"No module named..." errors:**
- Make sure all packages installed correctly
- Try reinstalling: `pip install --upgrade [package-name]`

**Google authentication not working:**
- Make sure `credentials.json` is in the Scripts folder
- Delete `token.json` and try authenticating again

**No weather data collected:**
- Check your internet connection
- Verify the National Weather Service API is working
- Make sure you're following the 1-hour minimum interval

**Analysis shows "No data found":**
- Make sure you have at least one day of collected data
- Check that files exist in the `raw_weather_json` folder
- Verify the date format in analysis commands

**Cron jobs not running:**
- Check that paths in crontab are absolute (full paths)
- Verify Python path with `which python3`
- Check log files for error messages

### Monitoring Your System

**Check collection is working:**
- Look for new files in `raw_weather_json` every hour
- Check your Google Drive folder for uploaded files
- Review `collection.log` for any errors

**Check analysis is working:**
- Look for new files in `daily_analysis`, `daily_verification`, and `center_reports` each morning
- Review `analysis.log` for any errors
- Verify that yesterday's date appears in new analysis files

**Data quality indicators:**
- Excellent: 23-24 hourly reports per day
- Good: 19-22 hourly reports per day
- Fair: 12-18 hourly reports per day
- Poor: 6-11 hourly reports per day

## Data Usage and Privacy

- This system only collects publicly available weather data
- No personal information is collected or stored
- All data comes from the National Weather Service public API
- Data is stored in your personal Google Drive account
- Reports are suitable for legal proceedings and public transparency

## Getting Help

If you encounter issues:

1. Check that all files are in the correct folders
2. Verify your Google Drive folder ID is correct
3. Make sure you're following the scheduling rules (hourly for collection, daily for analysis)
4. Check your internet connection is stable
5. Review log files for specific error messages

This complete system helps monitor weather conditions at detention facilities to ensure transparency and accountability in detention conditions through automated data collection, rigorous analysis, and legal documentation.

**Remember: Only run data collection once per hour and analysis once per day to respect the National Weather Service's public API.**
