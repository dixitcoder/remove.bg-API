from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from rembg import remove
from pyngrok import ngrok  # Import ngrok
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the POST request has a file
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']

    # If no file is selected
    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the input image
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_' + file.filename)

        file.save(input_path)

        # Remove the background
        with open(input_path, 'rb') as input_file:
            input_image = input_file.read()
            result = remove(input_image)

        # Save the processed image
        with open(output_path, 'wb') as output_file:
            output_file.write(result)

        # Render the template with the processed image's filename to display and download
        return render_template('index.html', processed_image='output_' + file.filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Start ngrok tunnel
    url = ngrok.connect(5000)  # This will expose the local Flask app on port 5000
    print(f" * ngrok tunnel accessible at: {url}")

    app.run()
