# 🏠 HomeHunt Data Collector

A powerful web-based apartment scraping tool that extracts property listings from Apartments.com and automatically uploads the data to Google Sheets. Built with Python, Flask, and Selenium for seamless apartment hunting.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![Selenium](https://img.shields.io/badge/selenium-v4.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🌐 **Web Interface**: Clean, responsive Flask web application
- 🤖 **Automated Scraping**: Extract apartment listings with Selenium WebDriver
- 📊 **Google Sheets Integration**: Automatic data upload to Google Sheets
- 📱 **Real-time Progress**: Live progress tracking with visual feedback
- 💾 **CSV Backup**: Local CSV files as backup storage
- 🔍 **Advanced Filtering**: Filter by location, price, bedrooms, and more
- 🚀 **Easy Setup**: Simple installation and configuration process
- 🛡️ **Error Handling**: Robust error handling and recovery mechanisms

## 🖼️ Screenshots

### Web Interface
The clean, modern web interface makes apartment hunting effortless:

#### Main Interface - Data Field Selection
![Main Interface](<img width="1905" height="1192" alt="Image" src="https://github.com/user-attachments/assets/8edfdcdb-ea15-4e2b-bb29-f2fa8b4c2839" />)

**Features shown:**
- 🏠 **Professional branding** with house icon and clean typography
- 📋 **Data Field Selection** with intuitive checkboxes:
  - 💰 Price Information (with money bag icon)
  - 📍 Property Address (with location pin icon)  
  - 🛏️ Bedrooms Count (with bed icon)
  - 🚿 Bathrooms Count (with shower icon)
  - 🔗 Property URL (with link icon)
- 🎨 **Modern UI design** with purple gradient background
- ▶️ **Prominent "START DATA COLLECTION" button** for easy access

#### Success State - Results Display  
![Results Display](screenshots/results-display.png)

**Features shown:**
- ✅ **Success notification** with clear status message
- 📊 **Property count display**: "Found 15 properties (loaded from CSV)"
- 📈 **Google Sheets integration** with direct access button
- 🎯 **Clean results presentation** in an easy-to-read format
- 💚 **Visual success indicators** with checkmarks and green styling

### Key Interface Benefits:
- **Intuitive Design**: Clear icons and labels make the interface self-explanatory
- **Real-time Feedback**: Live progress updates and success notifications
- **Professional Appearance**: Modern styling suitable for business use
- **Mobile-Friendly**: Responsive design works on all screen sizes
- **Accessibility**: High contrast and clear typography for easy reading

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Google Cloud Platform account (for Google Sheets integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/homehunt-data-collector.git
   cd homehunt-data-collector
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets integration**
   - Follow the detailed guide in `GOOGLE_SETUP_GUIDE.md`
   - Download your `credentials.json` file
   - Place it in the project root directory

4. **Run the application**
   ```bash
   python app.py
   ```
   
   Or use the batch file on Windows:
   ```bash
   start_webapp.bat
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📋 Usage

### Web Interface Method (Recommended)

1. **Start the web application**
   ```bash
   python app.py
   ```

2. **Access the interface**
   - Open your browser and go to `http://localhost:5000`
   
3. **Enter search criteria**
   - Location (e.g., "Brooklyn, NY", "Manhattan", "Queens")
   - Price range (optional)
   - Number of bedrooms (optional)
   - Additional filters

4. **Start scraping**
   - Click "Start Scraping"
   - Watch real-time progress updates
   - View extracted properties as they're found

5. **Access your data**
   - Click the Google Sheets link when scraping completes
   - Download the local CSV backup if needed

### Command Line Method

For advanced users or automation:

```bash
python main.py
```

## 📁 Project Structure

```
homehunt-data-collector/
├── app.py                 # Flask web application
├── main.py               # Main scraping script 
├── requirements.txt      # Python dependencies
├── credentials.json      # Google API credentials (create this)
├── GOOGLE_SETUP_GUIDE.md # Google Sheets setup instructions
├── start_webapp.bat      # Windows batch file to start app
├── templates/
│   └── index.html        # Web interface template
├── apartments_properties_*.csv  # Generated CSV files

```

## 🔧 Configuration

### Google Sheets Setup

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project

2. **Enable Google Sheets API**
   - Navigate to APIs & Services > Library
   - Search for "Google Sheets API" and enable it

3. **Create Service Account**
   - Go to APIs & Services > Credentials
   - Create a new service account
   - Download the JSON key file as `credentials.json`

4. **Share your Google Sheet**
   - Create a new Google Sheet
   - Share it with the service account email from `credentials.json`
   - Give it "Editor" permissions

### Environment Variables (Optional)

Create a `.env` file for additional configuration:

```env
FLASK_DEBUG=True
SHEET_ID=your_google_sheet_id_here
DEFAULT_LOCATION=New York, NY
```

## 🛠️ Technical Details

### Technologies Used

- **Backend**: Python 3.7+, Flask 2.0+
- **Web Scraping**: Selenium WebDriver, ChromeDriver
- **Data Processing**: Pandas, CSV
- **Google Integration**: Google Sheets API v4
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Modern CSS with flexbox and animations

### Key Features Implementation

- **Subprocess Management**: Runs scraping in background process
- **Real-time Updates**: AJAX polling for live progress updates
- **Unicode Handling**: Proper encoding for international characters
- **Error Recovery**: Automatic retry mechanisms and fallback options
- **Cross-platform**: Works on Windows, macOS, and Linux

## 📊 Data Output

### CSV Format
```csv
Price,Address,Beds,Baths,URL
"$3,127 - $9,000","499 President St, Brooklyn, NY 11215",Studio - 2 Beds,1 bath,https://www.apartments.com/...
```

### Google Sheets Integration
- Automatic column formatting
- Clickable property URLs
- Sortable and filterable data
- Real-time collaboration support

## 🚨 Important Notes

### Rate Limiting & Ethics
- This tool is for personal use and research purposes
- Respect robots.txt and website terms of service
- Implement delays between requests to avoid overloading servers
- Use responsibly and ethically

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test on multiple platforms if possible
- Update documentation for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Selenium WebDriver** - For web automation capabilities
- **Flask** - For the lightweight web framework
- **Google Sheets API** - For seamless data integration
- **Apartments.com** - For providing property listing data

## 📧 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section above**
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information:
   - Operating system and Python version
   - Complete error message
   - Steps to reproduce the problem

## 🔄 Updates & Roadmap

### Recent Updates
- ✅ Added web interface
- ✅ Real-time progress tracking
- ✅ Unicode error handling
- ✅ Google Sheets integration
- ✅ CSV backup functionality

### Planned Features
- 🔄 Multiple property websites support
- 🔄 Advanced filtering options
- 🔄 Email notifications
- 🔄 Scheduled scraping
- 🔄 Database storage option
- 🔄 Property comparison tools

## ⭐ Star History

If this project helps you find your perfect home, please consider giving it a star! ⭐

---

**Happy House Hunting! 🏡**

*Made with ❤️ for apartment hunters everywhere*

