from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Define the folder where the uploaded file will be saved
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file is present in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Check if the file is a PDF
    if file and file.filename.endswith('.pdf'):
        # Save the file with the name "input_pdf.pdf"
        file_path = os.path.join(UPLOAD_FOLDER, 'input_pdf.pdf')
        file.save(file_path)

        # Get the selected languages from the form data
        languages = request.form.getlist('language')[0]

        # Run the Python script with the saved file and selected languages
        try:
            # Construct the command to run the Python script
            print(languages)
            command = ["python", "main.py", "uploads\\input_pdf.pdf", "-l", languages]
            result = subprocess.run(command, capture_output=False, text=True)

            # Check if the script ran successfully
            if result.returncode == 0:
                summary = result.stdout  # Use the script's output as the summary
                return jsonify({'summary': summary}), 200
                # return jsonify({'error': success}), 400
            else:
                return jsonify({'error': result.stderr}), 400
        except Exception as e:
            return jsonify({'error': f'Failed to run script: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

if __name__ == '__main__':
    app.run(debug=True)