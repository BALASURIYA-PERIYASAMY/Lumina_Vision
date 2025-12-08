from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import sys
import os

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.detector import ObjectDetector
from src.reader import TextReader

app = Flask(__name__)
CORS(app)

# Initialize modules globally (warm start)
print("Initializing AI modules...")
detector = ObjectDetector()
reader = TextReader()
print("AI modules ready.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        image_data = data.get('image')
        mode = data.get('mode', 'detect') # 'detect' or 'read'

        if not image_data:
            return jsonify({'error': 'No image data'}), 400

        # Decode base64 image
        encoded_data = image_data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result_text = ""
        
        if mode == 'detect':
            detections = detector.detect(img)
            result_text = detector.describe_scene(detections)
        elif mode == 'read':
            result_text = reader.read_text(img)
            if not result_text:
                result_text = "No text detected."
        else:
            return jsonify({'error': 'Invalid mode'}), 400

        return jsonify({'result': result_text})

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Network Utility to find local IP
    import socket
    import qrcode
    
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    local_ip = get_local_ip()
    url = f"http://{local_ip}:5000"
    
    print("\n" + "="*40)
    print(f"MOBILE ACCESS LINK: {url}")
    print("="*40)
    
    print(f"MOBILE ACCESS LINK: {url}")
    print("="*40)

    # Host 0.0.0.0 allows access from other devices on network
    app.run(host='0.0.0.0', port=5000, debug=True)
