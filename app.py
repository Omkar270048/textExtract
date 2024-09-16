from flask import Flask, render_template, request, redirect, url_for
import os
from text_extractor import extract_text_from_image

app = Flask(__name__)

# Path to save uploaded images
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'images[]' not in request.files:
            return 'No file part'

        files = request.files.getlist('images[]')
        extracted_texts = {}
        for file in files:
            if file and allowed_file(file.filename):
                # Save the file
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Extract text using the module
                extracted_text = extract_text_from_image(filepath)
                extracted_texts[filename] = extracted_text

        return render_template('results.html', extracted_texts=extracted_texts)

    return render_template('index.html')

if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
