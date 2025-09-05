# Google Console Setup Guide for HomeHunt Data Collector
# Follow these steps for automatic Google Sheets uploads

## Step 1: Go to Google Cloud Console
1. Open your browser and go to: https://console.cloud.google.com/
2. Sign in with your Google account

## Step 2: Create a New Project
1. Click the project dropdown at the top (next to "Google Cloud")
2. Click "NEW PROJECT"
3. Enter project name: "HomeHunt Data Collector"
4. Click "CREATE"
5. Wait for the project to be created (30 seconds)

## Step 3: Enable Google Sheets API
1. In the left sidebar, click "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click on "Google Sheets API"
4. Click "ENABLE" button
5. Wait for it to enable (30 seconds)

## Step 4: Create Service Account Credentials
1. In the left sidebar, click "APIs & Services" > "Credentials"
2. Click "CREATE CREDENTIALS" at the top
3. Select "Service account"
4. Fill in the form:
   - Service account name: "homehunt-scraper-2025" (or add your initials like "homehunt-scraper-xyz")
   - Service account ID: (will auto-fill, or manually change it to be unique)
   - Description: "Service account for HomeHunt data scraper"
5. Click "CREATE AND CONTINUE"
6. Skip the optional steps by clicking "DONE"

## TROUBLESHOOTING: If "Service account ID already exists" error:
- Change the Service account name to something unique like:
  - "homehunt-scraper-2025"
  - "homehunt-scraper-[your initials]"
  - "homehunt-data-collector-v2"
- The system will auto-generate a unique ID
- Any unique name will work perfectly!

## Step 5: Generate and Download Key
1. In the Credentials page, find your service account
2. Click on the service account email (looks like: homehunt-scraper@...)
3. Go to the "KEYS" tab
4. Click "ADD KEY" > "Create new key"
5. Select "JSON" format
6. Click "CREATE"
7. A JSON file will download automatically

## Step 6: Setup the Credentials File
1. Rename the downloaded file to: "credentials.json"
2. Move it to your project folder: "d:\HomeHunt Data Collector\"
3. Make sure it's in the same folder as main.py

## Step 7: Share Your Google Sheet with the Service Account
1. Open the credentials.json file and find the "client_email" field
2. Copy the email address (looks like: homehunt-scraper-2025@...iam.gserviceaccount.com)
3. Go to your Google Sheet: https://docs.google.com/spreadsheets/d/1Qi9aB8jDuN6524b9seAXpvOjwzNHvc3xxJJm-aLRA9k/edit?usp=sharing
4. Click "Share" button (top right)
5. Paste the service account email
6. Set permission to "Editor"
7. Click "Send"

## Step 8: Install Required Package
1. Open PowerShell in your project folder
2. Run: pip install google-auth

## Step 9: Test the Setup
1. Run your scraper: python main.py
2. It should now automatically upload to your Google Sheet!

## Troubleshooting
- Make sure credentials.json is in the same folder as main.py
- Make sure you shared the sheet with the service account email
- Make sure the sheet URL is correct in your code

## What You'll Get
✅ Fully automated uploads to Google Sheets
✅ No more manual copy-paste
✅ Real-time data sharing
✅ Professional setup that works forever

Total time: 5-10 minutes
Difficulty: Easy (just clicking buttons)
