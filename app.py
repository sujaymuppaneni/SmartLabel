import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Lists of ingredients categorized by health impact
UNHEALTHY_INGREDIENTS = [
    'high fructose corn syrup', 'hfcs', 'artificial sweetener', 'aspartame',
    'saccharin', 'sucralose', 'monosodium glutamate', 'msg', 'trans fat',
    'hydrogenated oil', 'partially hydrogenated', 'sodium nitrite',
    'sodium benzoate', 'artificial color', 'red 40', 'yellow 5', 'yellow 6',
    'blue 1', 'blue 2', 'caramel color', 'bha', 'bht', 'propyl gallate',
    'tbhq', 'potassium bromate', 'sodium phosphate', 'carrageenan'
]

MODERATE_INGREDIENTS = [
    'sugar', 'corn syrup', 'dextrose', 'maltodextrin', 'modified food starch',
    'soy lecithin', 'natural flavor', 'artificial flavor', 'citric acid',
    'sodium chloride', 'salt', 'palm oil', 'canola oil', 'soybean oil',
    'corn oil', 'xanthan gum', 'guar gum', 'gelatin', 'yeast extract',
    'dextrin', 'glucose', 'fructose', 'maltose'
]


def allowed_file(filename):
    """Check if uploaded file has allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def preprocess_text(text):
    """Clean and preprocess extracted text."""
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep commas and parentheses
    text = re.sub(r'[^\w\s,()-]', '', text)
    return text.strip()


def extract_text_from_image(image_path):
    """Extract text from image using Tesseract OCR."""
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(img)
        
        # Preprocess the text
        processed_text = preprocess_text(text)
        
        return processed_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"


def analyze_ingredients(text):
    """Analyze ingredients and generate health rating."""
    # Count unhealthy and moderate ingredients
    unhealthy_count = 0
    moderate_count = 0
    found_unhealthy = []
    found_moderate = []
    
    # Check for unhealthy ingredients
    for ingredient in UNHEALTHY_INGREDIENTS:
        if ingredient in text:
            unhealthy_count += 1
            found_unhealthy.append(ingredient)
    
    # Check for moderate ingredients
    for ingredient in MODERATE_INGREDIENTS:
        if ingredient in text:
            moderate_count += 1
            found_moderate.append(ingredient)
    
    # Determine health rating
    if unhealthy_count >= 3:
        rating = "Avoid"
        rating_class = "danger"
        recommendation = "This product contains multiple unhealthy ingredients that may have negative health impacts. Consider avoiding this product."
    elif unhealthy_count >= 1:
        rating = "Moderate"
        rating_class = "warning"
        recommendation = "This product contains some concerning ingredients. Consume in moderation and consider healthier alternatives."
    elif moderate_count >= 5:
        rating = "Moderate"
        rating_class = "warning"
        recommendation = "This product contains several moderately processed ingredients. It's okay occasionally, but try to choose less processed options when possible."
    else:
        rating = "Healthy"
        rating_class = "success"
        recommendation = "This product appears to have relatively clean ingredients. A good choice for regular consumption."
    
    return {
        'rating': rating,
        'rating_class': rating_class,
        'recommendation': recommendation,
        'unhealthy_found': found_unhealthy,
        'moderate_found': found_moderate,
        'unhealthy_count': unhealthy_count,
        'moderate_count': moderate_count
    }


@app.route('/')
def index():
    """Render the home page with upload form."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis."""
    # Check if file was uploaded
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # Check if file was selected
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    # Check if file is allowed
    if file and allowed_file(file.filename):
        # Secure the filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(filepath)
        
        # Extract text from image
        extracted_text = extract_text_from_image(filepath)
        
        # Analyze ingredients
        analysis = analyze_ingredients(extracted_text)
        
        # Clean up - remove uploaded file
        try:
            os.remove(filepath)
        except (OSError, FileNotFoundError):
            pass
        
        # Render results
        return render_template('results.html',
                             extracted_text=extracted_text,
                             analysis=analysis)
    else:
        flash('Invalid file type. Please upload JPG or PNG images only.', 'error')
        return redirect(url_for('index'))


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the app
    # Debug mode should be disabled in production for security
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
