from flask import Flask, jsonify
from flask_cors import CORS  # Import the CORS package
import subprocess

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=['http://localhost:3000'])  # Allow requests from this origin

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Execute the Python script
        result = subprocess.run(['python', 'main_face.py'], capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500
        return jsonify({'message': 'Script executed successfully', 'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)