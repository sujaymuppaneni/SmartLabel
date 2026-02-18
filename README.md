# SmartLabel 🏷️
AI-Based Ingredient Health Rating System

## Overview

SmartLabel is a Flask-based web application that helps consumers make informed decisions about food products by analyzing ingredient labels. Upload an image of a food product's ingredient label, and our system will:

- Extract text using OCR (Tesseract)
- Analyze ingredients for health impact
- Generate a health rating (Healthy / Moderate / Avoid)
- Provide recommendations for healthier choices

## Features

- 📸 **Image Upload**: Support for JPG/PNG images up to 16MB
- 🔍 **OCR Processing**: Advanced text extraction using Tesseract OCR
- 🧪 **Ingredient Analysis**: Intelligent analysis against a database of unhealthy and processed ingredients
- ⭐ **Health Ratings**: Clear ratings with actionable recommendations
- 💻 **User-Friendly Interface**: Clean, responsive web design
- 🚀 **Fast Processing**: Quick analysis and results

## Prerequisites

Before running this application, ensure you have the following installed:

- Python 3.8 or higher
- Tesseract OCR

### Installing Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sujaymuppaneni/SmartLabel.git
   cd SmartLabel
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Flask application:**
   ```bash
   python app.py
   ```
   
   **For development with debug mode:**
   ```bash
   FLASK_DEBUG=true python app.py
   ```
   
   **Note:** Debug mode is disabled by default for security. Only enable it during development.

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Upload an ingredient label image:**
   - Click "Choose File" and select an image (JPG or PNG)
   - Click "Analyze Ingredients"
   - View the health rating and recommendations

## Configuration

The application supports the following environment variables:

- **SECRET_KEY**: Secret key for Flask session management (randomly generated if not set)
- **FLASK_DEBUG**: Set to `true` to enable debug mode (default: `false`)

**For production deployment:**
```bash
export SECRET_KEY="your-strong-random-secret-key"
python app.py
```

## How It Works

1. **Upload**: User uploads an image of a food product's ingredient label
2. **OCR Extraction**: Tesseract OCR extracts text from the image
3. **Preprocessing**: Text is cleaned and normalized for analysis
4. **Analysis**: Ingredients are matched against databases of:
   - Unhealthy ingredients (artificial additives, trans fats, etc.)
   - Moderate ingredients (processed sugars, oils, etc.)
5. **Rating Generation**: Based on findings:
   - **Healthy**: Minimal concerning ingredients
   - **Moderate**: Some processed or concerning ingredients
   - **Avoid**: Multiple unhealthy ingredients
6. **Results**: Display rating, recommendation, and detailed ingredient breakdown

## Project Structure

```
SmartLabel/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore file
├── templates/            # HTML templates
│   ├── index.html        # Home page with upload form
│   ├── results.html      # Analysis results page
│   └── about.html        # About page
├── static/               # Static files
│   └── css/
│       └── style.css     # Application styling
└── uploads/              # Temporary upload directory
```

## Technology Stack

- **Backend**: Flask (Python web framework)
- **OCR**: Tesseract OCR engine
- **Image Processing**: Pillow (PIL)
- **Frontend**: HTML5, CSS3, JavaScript
- **File Handling**: Werkzeug

## Health Rating Algorithm

The application categorizes ingredients into:

### Unhealthy Ingredients (Avoid)
- High fructose corn syrup (HFCS)
- Artificial sweeteners (aspartame, sucralose)
- Trans fats and hydrogenated oils
- Artificial colors and preservatives
- MSG and sodium additives

### Moderate Ingredients (Use Caution)
- Refined sugars and corn syrup
- Modified starches
- Natural and artificial flavors
- Processed oils
- Thickening agents

**Rating Logic:**
- 3+ unhealthy ingredients → **Avoid**
- 1-2 unhealthy ingredients → **Moderate**
- 5+ moderate ingredients → **Moderate**
- Otherwise → **Healthy**

## Security Features

- File type validation (only JPG/PNG allowed)
- Secure filename handling
- File size limits (16MB max)
- Automatic cleanup of uploaded files
- Input sanitization

## Limitations

- OCR accuracy depends on image quality
- Ingredient database is not exhaustive
- Analysis is educational, not medical advice
- Works best with clear, well-lit images

## Future Enhancements

- [ ] Expand ingredient database
- [ ] Add nutritional value analysis
- [ ] Support for multiple languages
- [ ] Mobile app version
- [ ] User accounts and history
- [ ] API endpoint for third-party integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This application provides general guidance on food ingredients and should not replace professional medical or nutritional advice. Always consult healthcare professionals for personalized dietary recommendations.

## Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ for healthier food choices
