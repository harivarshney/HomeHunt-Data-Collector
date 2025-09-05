"""
HomeHunt Data Collector - Web Interface
Simple web application for scraping real estate data
"""
from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import time
import os
import json
from datetime import datetime

app = Flask(__name__)

# Global variables for progress tracking
scraping_progress = {
    "status": "idle", 
    "current": 0, 
    "total": 0, 
    "message": "Ready to scrape",
    "properties": [],
    "sheet_url": None,
    "completed": False
}
scraping_thread = None

def scrape_with_subprocess(filters):
    """Run scraping using subprocess to avoid Unicode issues"""
    global scraping_progress
    
    try:
        scraping_progress["status"] = "running"
        scraping_progress["message"] = "Setting up Chrome browser..."
        scraping_progress["current"] = 0
        scraping_progress["total"] = 0
        scraping_progress["properties"] = []
        scraping_progress["completed"] = False
        
        # Create command to run main.py (your original file)
        import sys
        python_exe = sys.executable
        main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        cmd = [python_exe, main_py_path]
        
        scraping_progress["message"] = f"Starting main.py with command: {' '.join(cmd)}"
        
        # Run the subprocess with better error handling
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Combine stderr with stdout
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True,
                encoding='utf-8',  # Explicitly set UTF-8 encoding
                errors='replace',  # Replace problematic characters
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            scraping_progress["message"] = "Successfully started main.py process..."
        except Exception as e:
            scraping_progress["status"] = "error"
            scraping_progress["message"] = f"Failed to start main.py: {str(e)}"
            scraping_progress["completed"] = True
            return
        
        # Read output line by line
        output_lines = []
        collected_url = ""
        line_count = 0
        
        while True:
            try:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    output_lines.append(line)
                    line_count += 1
                    
                    # Debug: Show we're getting output
                    if line_count == 1:
                        scraping_progress["message"] = f"Process started! First line: {line[:50]}..."
                    elif line_count % 5 == 0:
                        scraping_progress["message"] = f"Processing... (line {line_count})"
                    
                    # Collect multi-line URLs
                    if "🔗 View your sheet:" in line or "View your sheet:" in line:
                        # Start collecting URL, might be split across lines
                        url_part = line.replace("🔗 View your sheet:", "").replace("View your sheet:", "").strip()
                        collected_url = url_part
                    elif collected_url and not collected_url.startswith("http") and "http" in line:
                        # Continue collecting URL from next line
                        collected_url += line.strip()
                    elif collected_url and collected_url.startswith("http"):
                        # We have a complete URL
                        scraping_progress["sheet_url"] = collected_url
                        collected_url = ""  # Reset
                    
                    # Update progress based on output
                    if "Starting Chrome browser" in line or "Opening Apartments.com" in line:
                        scraping_progress["message"] = "Setting up Chrome browser..."
                    elif "Waiting for page to load" in line:
                        scraping_progress["message"] = "Loading page..."
                    elif "Searching for property data" in line:
                        scraping_progress["message"] = "Searching for properties..."
                    elif "Found" in line and "properties using selector" in line:
                        try:
                            # Extract number of properties found
                            words = line.split()
                            for word in words:
                                if word.isdigit():
                                    scraping_progress["total"] = int(word)
                                    scraping_progress["message"] = f"Found {word} properties! Extracting data..."
                                    break
                        except:
                            pass
                    elif "Total property containers found:" in line:
                        try:
                            # Extract total containers
                            total = int(line.split(":")[-1].strip())
                            scraping_progress["total"] = total
                            scraping_progress["message"] = f"Processing {total} properties..."
                        except:
                            pass
                    elif "Processing property" in line:
                        try:
                            # Extract current property number (format: "Processing property 1/15...")
                            parts = line.split()
                            for part in parts:
                                if "/" in part:
                                    current, total = part.split("/")
                                    current = current.replace("...", "")
                                    scraping_progress["current"] = int(current)
                                    scraping_progress["total"] = int(total)
                                    scraping_progress["message"] = f"Extracting property {current}/{total}..."
                                    break
                        except:
                            pass
                    elif "Property" in line and "$" in line and "|" in line:
                        try:
                            # Parse property line: "Property 1: $3,127 - $9,000 | 499 President St, Brooklyn, NY 11215 | Studio - 2 Beds | 1 bath"
                            parts = line.split(" | ")
                            if len(parts) >= 4:
                                price_part = parts[0].split(": ", 1)[1] if ": " in parts[0] else parts[0]
                                address = parts[1]
                                beds = parts[2]
                                baths = parts[3]
                                
                                property_data = {
                                    "Price": price_part,
                                    "Address": address,
                                    "Beds": beds,
                                    "Baths": baths,
                                    "URL": "See CSV file"
                                }
                                scraping_progress["properties"].append(property_data)
                        except:
                            pass
                    elif "Successfully extracted" in line and "properties" in line:
                        try:
                            # Extract final count
                            words = line.split()
                            for word in words:
                                if word.isdigit():
                                    scraping_progress["message"] = f"Successfully extracted {word} properties!"
                                    break
                        except:
                            pass
                    elif "Data uploaded successfully" in line:
                        scraping_progress["message"] = "Data uploaded to Google Sheets successfully!"
                    elif "Data saved to:" in line:
                        scraping_progress["message"] = "Data saved locally and uploading to Google Sheets..."
                    elif "Error:" in line:
                        scraping_progress["message"] = f"Error: {line}"
            except UnicodeDecodeError as e:
                # Handle Unicode decoding errors specifically
                scraping_progress["message"] = f"Unicode error reading output: {str(e)} - continuing..."
                continue
            except Exception as e:
                # Handle any other errors while reading output
                scraping_progress["message"] = f"Error reading output: {str(e)}"
                break
        
        # Wait for process to complete with timeout
        try:
            process.wait(timeout=300)  # 5 minute timeout
        except subprocess.TimeoutExpired:
            scraping_progress["status"] = "error"
            scraping_progress["message"] = "Process timed out after 5 minutes"
            scraping_progress["completed"] = True
            process.kill()
            return
        
        if process.returncode == 0:
            if scraping_progress["properties"]:
                scraping_progress["status"] = "completed"
                scraping_progress["message"] = f"Success! Found {len(scraping_progress['properties'])} properties"
                scraping_progress["completed"] = True
                # Set the default Google Sheets URL as fallback
                if not scraping_progress["sheet_url"]:
                    scraping_progress["sheet_url"] = "https://docs.google.com/spreadsheets/d/1Qi9aB8jDuN6524b9seAXpvOjwzNHvc3xxJJm-aLRA9k/edit?usp=sharing"
            else:
                # Try to read from latest CSV file as backup
                try:
                    import pandas as pd
                    csv_files = [f for f in os.listdir('.') if f.startswith('apartments_properties_') and f.endswith('.csv')]
                    if csv_files:
                        latest_file = max(csv_files, key=os.path.getctime)
                        df = pd.read_csv(latest_file)
                        for _, row in df.iterrows():
                            property_data = {
                                "Price": row.get('Price', 'N/A'),
                                "Address": row.get('Address', 'N/A'),
                                "Beds": row.get('Beds', 'N/A'),
                                "Baths": row.get('Baths', 'N/A'),
                                "URL": row.get('URL', 'N/A')
                            }
                            scraping_progress["properties"].append(property_data)
                        
                        scraping_progress["status"] = "completed"
                        scraping_progress["message"] = f"Success! Found {len(scraping_progress['properties'])} properties (loaded from CSV)"
                        scraping_progress["completed"] = True
                        # Set the default Google Sheets URL as fallback
                        if not scraping_progress["sheet_url"]:
                            scraping_progress["sheet_url"] = "https://docs.google.com/spreadsheets/d/1Qi9aB8jDuN6524b9seAXpvOjwzNHvc3xxJJm-aLRA9k/edit?usp=sharing"
                    else:
                        scraping_progress["status"] = "completed"
                        scraping_progress["message"] = "Completed but no properties found"
                        scraping_progress["completed"] = True
                except Exception as e:
                    scraping_progress["status"] = "completed"
                    scraping_progress["message"] = "Completed - check CSV files for data"
                    scraping_progress["completed"] = True
        else:
            # Check for errors
            error_output = process.stderr.read()
            scraping_progress["status"] = "error"
            scraping_progress["message"] = f"Error occurred during scraping"
            scraping_progress["completed"] = True
            
    except Exception as e:
        scraping_progress["status"] = "error"
        scraping_progress["message"] = f"Error: {str(e)}"
        scraping_progress["completed"] = True

@app.route('/')
def index():
    """Main page with checkboxes and scraping interface"""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def start_scraping():
    """Start scraping with selected filters"""
    global scraping_thread, scraping_status
    
    if scraping_progress["status"] == "running":
        return jsonify({"error": "Data collection already in progress!"})
    
    # Get selected filters from checkboxes
    filters = request.form.getlist('filters')
    
    # Start scraping in background
    scraping_thread = threading.Thread(target=scrape_with_subprocess, args=(filters,))
    scraping_thread.daemon = True
    scraping_thread.start()
    
    return jsonify({"success": True, "message": "Data collection started!"})

@app.route('/progress')
def get_progress():
    """Get current scraping progress"""
    return jsonify(scraping_progress)

@app.route('/properties')
def get_properties():
    """Get collected properties data"""
    try:
        # Try to read the latest CSV file
        csv_files = [f for f in os.listdir('.') if f.startswith('apartments_properties_') and f.endswith('.csv')]
        if csv_files:
            latest_file = max(csv_files, key=os.path.getctime)
            import pandas as pd
            df = pd.read_csv(latest_file)
            properties = df.to_dict('records')
            return jsonify({"properties": properties})
        else:
            return jsonify({"properties": []})
    except Exception as e:
        return jsonify({"properties": [], "error": str(e)})

if __name__ == '__main__':
    print("🏠 HomeHunt Data Collector Web Interface")
    print("🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
