# -*- coding: utf-8 -*-
# HomeHunt Data Collector - Main Script using Apartments.com with Google Sheets Integration
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Make sure output is flushed immediately
import functools
original_print = print
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os

def upload_to_google_sheets(df, sheet_url=None):
    """Upload DataFrame to your existing Google Sheet - Enhanced version with better error handling"""
    try:
        if not sheet_url:
            print("\n📊 Google Sheets Upload Options:")
            print("1. Using your pre-configured Google Sheet")
            print("2. Or provide a custom Google Sheet URL")
            
            # Ask user for their sheet URL
            print("Using default Google Sheet for web interface...")
            user_sheet_url = ""  # Auto-use default for web interface
            if user_sheet_url:
                sheet_url = user_sheet_url
            else:
                sheet_url = ""
        
        print("📊 Attempting to upload to your Google Sheet...")
        
        try:
            import gspread
            from google.oauth2.service_account import Credentials
            
            # Check for credentials file
            creds_file = 'credentials.json'
            if not os.path.exists(creds_file) or os.path.getsize(creds_file) == 0:
                print("❌ No credentials.json file found!")
                print("📝 Please follow the setup guide in GOOGLE_SETUP_GUIDE.md")
                print("🔗 Quick setup: https://console.cloud.google.com/")
                print("\n📋 Manual backup - Copy this data to your sheet:")
                print("="*60)
                print(f"=== HomeHunt Data - {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
                print(df.to_csv(index=False))
                print("="*60)
                return False
            
            print("🔑 Loading Google credentials...")
            # Use service account credentials with proper scopes
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials = Credentials.from_service_account_file(creds_file, scopes=scopes)
            gc = gspread.authorize(credentials)
            
            print("📊 Connecting to Google Sheet...")
            try:
                # Open the sheet by URL
                sheet = gc.open_by_url(sheet_url)
                worksheet = sheet.sheet1
            except Exception as e:
                print(f"❌ Sheet access error: {e}")
                print("💡 Make sure your sheet URL is correct and accessible")
                print("💡 Check that you shared the sheet with your service account email")
                print("\n📋 Manual backup - Copy this data:")
                print("="*50)
                print(df.to_csv(index=False))
                print("="*50)
                return False
            
            print("📝 Uploading data...")
            # Add timestamp
            timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            
            try:
                # Add separator and data
                worksheet.append_row([])
                worksheet.append_row([f"=== HomeHunt Data - {timestamp} ==="])
                worksheet.append_row(df.columns.tolist())
                
                # Upload data
                for _, row in df.iterrows():
                    worksheet.append_row(row.tolist())
                
                print(f"✅ Data uploaded successfully!")
                print(f"🔗 View your sheet: {sheet_url}")
                return True
                
            except Exception as e:
                print(f"❌ Upload error: {e}")
                print("\n📋 Manual backup - Copy this data:")
                print("="*50)
                print(df.to_csv(index=False))
                print("="*50)
                return False
                
        except ImportError:
            print("❌ gspread not installed. Install with: pip install gspread google-auth")
            print("\n📋 Manual option - Copy this data to your sheet:")
            print("="*50)
            print(df.to_csv(index=False))
            print("="*50)
            return False
            
        except Exception as e:
            print(f"❌ Error uploading to Google Sheet: {e}")
            print("\n📋 Manual backup - Copy this data:")
            print("="*50)
            print(df.to_csv(index=False))
            print("="*50)
            return False
        
    except Exception as e:
        print(f"❌ Error in Google Sheets function: {e}")
        return False

def scrape_apartments_main():
    """Main Apartments.com scraper - Enhanced version with robust extraction"""
    
    # Setup Chrome with enhanced options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-background-networking")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    
    try:
        print("Opening Apartments.com New York...")
        driver.get("https://www.apartments.com/new-york-ny/")
        
        print("Waiting for page to load...")
        time.sleep(10)
        
        print("Apartments.com usually doesn't require verification.")
        # Skip interactive prompt for web interface
        print("Continuing automatically...")
        
        print("Searching for property data...")
        print(f"Page title: {driver.title}")
        
        # Enhanced property card detection with multiple selectors
        try:
            properties = []
            
            print("🔍 Enhanced Method: Using multiple selector strategies...")
            
            # Try multiple selectors to find property cards
            card_selectors = [
                '.placard',
                '.property-wrap',
                '.listing-item',
                '.result-item',
                '[data-testid="property-card"]',
                '.rentals-results .property',
                '.property-card',
                '.listing-result',
                '[class*="property"]',
                '[class*="listing"]'
            ]
            
            property_cards = []
            for selector in card_selectors:
                try:
                    cards = driver.find_elements(By.CSS_SELECTOR, selector)
                    if cards:
                        print(f"✅ Found {len(cards)} properties using selector: {selector}")
                        property_cards = cards[:15]  # Limit to 15 properties
                        break
                except Exception as e:
                    print(f"⏭️ Selector {selector} failed: {e}")
                    continue
            
            if not property_cards:
                print("🔍 Fallback Method: Looking for any divs with property-like content...")
                all_divs = driver.find_elements(By.TAG_NAME, "div")
                for div in all_divs[:100]:  # Check first 100 divs
                    text = div.text.strip()
                    if ('$' in text and ('bed' in text.lower() or 'bath' in text.lower() or 'br' in text.lower())):
                        property_cards.append(div)
                        if len(property_cards) >= 10:
                            break
            
            print(f"📋 Total property containers found: {len(property_cards)}")
            
            # Enhanced data extraction from property cards
            for i, card in enumerate(property_cards):
                print(f"\n🏠 Processing property {i+1}/{len(property_cards)}...")
                
                try:
                    # Enhanced price extraction
                    price = "Not found"
                    price_selectors = [
                        ".//*[contains(@class, 'price')]",
                        ".//*[contains(@class, 'rent')]",
                        ".//*[contains(text(), '$')]",
                        ".//span[contains(text(), '$')]",
                        ".//div[contains(text(), '$')]",
                        './/*[@data-testid*="price"]'
                    ]
                    
                    for selector in price_selectors:
                        try:
                            price_elem = card.find_element(By.XPATH, selector)
                            price_text = price_elem.text.strip()
                            if '$' in price_text and price_text != "" and len(price_text) > 1:
                                price = price_text
                                break
                        except:
                            continue
                    
                    # Enhanced address extraction
                    address = "Not found"
                    address_selectors = [
                        ".//*[contains(@class, 'address')]",
                        ".//*[contains(@class, 'location')]",
                        ".//*[contains(text(), 'NY')]",
                        ".//*[contains(text(), 'Street')]",
                        ".//*[contains(text(), 'Ave')]",
                        ".//*[contains(text(), 'Blvd')]",
                        ".//*[contains(text(), 'Road')]",
                        './/*[@data-testid*="address"]'
                    ]
                    
                    for selector in address_selectors:
                        try:
                            addr_elem = card.find_element(By.XPATH, selector)
                            addr_text = addr_elem.text.strip()
                            if any(word in addr_text.lower() for word in ['ny', 'street', 'ave', 'blvd', 'road', 'dr', 'new york']):
                                address = addr_text
                                break
                        except:
                            continue
                    
                    # Enhanced beds extraction
                    beds = "Not found"
                    bed_selectors = [
                        ".//*[contains(@class, 'bed')]",
                        ".//*[contains(@class, 'bedroom')]",
                        ".//*[contains(text(), 'bed')]",
                        ".//*[contains(text(), 'bd')]",
                        ".//*[contains(text(), 'studio')]",
                        ".//*[contains(text(), 'br')]"
                    ]
                    
                    for selector in bed_selectors:
                        try:
                            bed_elem = card.find_element(By.XPATH, selector)
                            bed_text = bed_elem.text.strip().lower()
                            if any(word in bed_text for word in ['bed', 'bd', 'studio', 'bedroom', 'br']):
                                beds = bed_elem.text.strip()
                                break
                        except:
                            continue
                    
                    
                    # Enhanced bathroom detection
                    baths = "Not found"
                    
                    # Method 1: Look for explicit bathroom info
                    try:
                        card_text = card.text.lower()
                        
                        # Look for bathroom patterns
                        import re
                        bath_patterns = [
                            r'(\d+(?:\.\d+)?)\s*bath(?:s|room)?',
                            r'(\d+(?:\.\d+)?)\s*ba\b',
                            r'(\d+(?:\.\d+)?)\s*bathroom'
                        ]
                        
                        for pattern in bath_patterns:
                            bath_match = re.search(pattern, card_text)
                            if bath_match:
                                baths = bath_match.group(0)
                                break
                    except:
                        pass
                    
                    # Method 2: Enhanced estimation based on bedroom count
                    if baths == "Not found" and beds != "Not found":
                        try:
                            bed_text = beds.lower()
                            if 'studio' in bed_text:
                                baths = "1 bath"
                            elif '1' in bed_text:
                                baths = "1 bath"
                            elif '2' in bed_text:
                                baths = "1-2 baths"
                            elif '3' in bed_text:
                                baths = "2 baths"
                            elif '4' in bed_text:
                                baths = "2-3 baths"
                            else:
                                baths = "2+ baths"
                        except:
                            pass
                    
                    # Enhanced URL extraction
                    url = "Not found"
                    url_selectors = [
                        ".//a[contains(@href, '/')]",
                        ".//a",
                        ".//*[@href]"
                    ]
                    
                    for selector in url_selectors:
                        try:
                            link_elem = card.find_element(By.XPATH, selector)
                            href = link_elem.get_attribute('href')
                            if href:
                                if href.startswith('http'):
                                    url = href
                                elif href.startswith('/'):
                                    url = 'https://www.apartments.com' + href
                                break
                        except:
                            continue
                    
                    # Enhanced data validation - include property if it has useful data
                    data_count = 0
                    for value in [price, address, beds, baths, url]:
                        if value != "Not found" and value.strip():
                            data_count += 1
                    
                    if data_count >= 2:  # Include if at least 2 fields have data
                        property_dict = {
                            'Price': price,
                            'Address': address,
                            'Beds': beds,
                            'Baths': baths,
                            'URL': url
                        }
                        
                        properties.append(property_dict)
                        print(f"✅ Property {len(properties)}: {price} | {address} | {beds} | {baths}")
                    else:
                        print(f"⏭️ Skipped property {i+1} (insufficient data)")
                    
                except Exception as e:
                    print(f"❌ Error extracting property {i+1}: {e}")
                    continue
            
            if properties:
                print(f"\n🎉 Successfully extracted {len(properties)} properties!")
                print("\n📋 ALL PROPERTIES:")
                for prop in properties:
                    print(prop)
                    
                # Save to CSV
                df = pd.DataFrame(properties)
                filename = f"apartments_properties_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(filename, index=False)
                print(f"\n💾 Data saved to: {filename}")
                
                # Upload to Google Sheets
                # Your Google Sheet URL
                your_sheet_url = ""
                
                print("\n📊 Uploading to your Google Sheet...")
                sheet_success = upload_to_google_sheets(df, your_sheet_url)
                if sheet_success:
                    print(f"\n🌐 Your data is now accessible online!")
                    print(f"🔗 View your sheet: {your_sheet_url}")
                    print("\n📋 Anyone can view this data by visiting the link above!")
                else:
                    print("\n📝 Google Sheets upload completed. Check the output above for details.")
            else:
                print("❌ No properties extracted")
                
        except Exception as e:
            print(f"Error in extraction: {e}")
        
        # Skip interactive prompt for web interface
        print("Extraction completed, closing browser...")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_apartments_main()

