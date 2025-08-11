#!/usr/bin/env python3
# bulk_drive_uploader.py
# Upload all missing weather files to Google Drive

import os
import json
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Same configuration as your main script
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
DRIVE_FOLDER_ID = 'Find this in the browser address of your google folder'

def authenticate_google_drive():
    """Authenticate with Google Drive"""
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

def get_existing_files_in_drive(service, folder_id):
    """Get list of files already in Google Drive folder"""
    try:
        query = f"parents in '{folder_id}' and trashed=false"
        results = service.files().list(
            q=query,
            fields="files(name, id, createdTime)"
        ).execute()
        
        files = results.get('files', [])
        existing_files = set()
        
        for file in files:
            existing_files.add(file['name'])
        
        print(f" Found {len(existing_files)} files already in Google Drive")
        return existing_files
        
    except Exception as e:
        print(f" Could not check existing files: {e}")
        return set()

def upload_file_to_drive(service, file_path, folder_id):
    """Upload a single file to Google Drive"""
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
        
        return file.get('id')
        
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return None

def find_local_weather_files():
    """Find all local weather report files"""
    local_files = []
    raw_dir = "../raw_weather_json"
    
    if not os.path.exists(raw_dir):
        print(f" Directory not found: {raw_dir}")
        return []
    
    for filename in os.listdir(raw_dir):
        if filename.startswith("consolidated_weather_report_") and filename.endswith(".json"):
            file_path = os.path.join(raw_dir, filename)
            file_info = {
                'path': file_path,
                'name': filename,
                'size': os.path.getsize(file_path),
                'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            }
            local_files.append(file_info)
    
    # Sort by modification time (oldest first)
    local_files.sort(key=lambda x: x['modified'])
    
    print(f" Found {len(local_files)} local weather report files")
    return local_files

def main():
    """Upload all missing weather files to Google Drive"""
    print(" BULK GOOGLE DRIVE UPLOADER")
    print("=" * 50)
    
    # Authenticate
    try:
        print(" Authenticating with Google Drive...")
        service = authenticate_google_drive()
        print(" Authentication successful")
    except Exception as e:
        print(f" Authentication failed: {e}")
        return
    
    # Get existing files in Drive
    existing_files = get_existing_files_in_drive(service, DRIVE_FOLDER_ID)
    
    # Find local files
    local_files = find_local_weather_files()
    
    if not local_files:
        print(" No local weather files found")
        return
    
    # Find files that need uploading
    files_to_upload = []
    for file_info in local_files:
        if file_info['name'] not in existing_files:
            files_to_upload.append(file_info)
    
    print(f"\n Files to upload: {len(files_to_upload)}")
    print(f"  Files already in Drive: {len(local_files) - len(files_to_upload)}")
    
    if not files_to_upload:
        print(" All files are already uploaded!")
        return
    
    # Show date range
    if files_to_upload:
        oldest = files_to_upload[0]['modified']
        newest = files_to_upload[-1]['modified']
        print(f"📅 Date range: {oldest.strftime('%Y-%m-%d %H:%M')} to {newest.strftime('%Y-%m-%d %H:%M')}")
    
    # Ask for confirmation
    print(f"\n Upload {len(files_to_upload)} files to Google Drive?")
    response = input("Type 'yes' to continue: ").strip().lower()
    
    if response != 'yes':
        print(" Upload cancelled")
        return
    
    # Upload files
    print(f"\n Starting upload...")
    success_count = 0
    
    for i, file_info in enumerate(files_to_upload, 1):
        print(f"[{i}/{len(files_to_upload)}] {file_info['name']} ", end="")
        
        file_id = upload_file_to_drive(service, file_info['path'], DRIVE_FOLDER_ID)
        
        if file_id:
            print("✅")
            success_count += 1
        else:
            print("❌")
        
        # Small delay to be polite to Google's API
        if i % 10 == 0:
            print(f"   (Pausing briefly after {i} uploads...)")
            import time
            time.sleep(2)
    
    # Summary
    print(f"\n UPLOAD SUMMARY")
    print(f" Successful uploads: {success_count}")
    print(f" Failed uploads: {len(files_to_upload) - success_count}")
    print(f" Google Drive folder: https://drive.google.com/drive/folders/{DRIVE_FOLDER_ID}")
    
    if success_count > 0:
        print(" Upload complete! Check your Google Drive folder.")

if __name__ == "__main__":
    main()
