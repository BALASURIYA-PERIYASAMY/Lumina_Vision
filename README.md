# Lumina Vision
**Premium AI Assistant for the Visually Impaired**

Lumina Vision is an advanced assistive technology application designed to help visually impaired individuals navigate their surroundings. It uses Artificial Intelligence to "see" the world, providing real-time audio feedback about objects, scenes, and text.

## 🌟 Key Features
*   **Object Detection**: Identifies objects in real-time using YOLOv8 (e.g., "Person", "Chair", "Indian Rupee").
*   **OCR (Text Reading)**: Reads printed text from books, signs, and screens using Tesseract OCR.
*   **Indian Currency Recognition**: Trained to identify Indian notes (10, 20, 50, 100, 200, 500, 2000).
*   **Voice Feedback**: Automaticaly announces findings using Text-to-Speech (TTS).
*   **Dual Platforms**: 
    1.  **Web App (PWA)**: Works on any browser (PC/Mobile) with a premium Glassmorphism UI.
    2.  **Native Mobile App**: Python-based (KivyMD) app source code for a true mobile experience.

## 🛠️ Technology Stack
*   **Backend**: Python, Flask, OpenCV
*   **AI Models**: YOLOv8m (Medium) for detection, Tesseract 5.0 for OCR.
*   **Frontend (Web)**: HTML5, CSS3 (Glassmorphism), JavaScript (Web Speech API).
*   **Frontend (Mobile)**: KivyMD (Python Material Design).

## 🚀 Installation

### Prerequisites
1.  **Python 3.10+** installed.
2.  **Tesseract OCR** installed on your system.
    *   Window: `winget install -e --id UB-Mannheim.TesseractOCR`
    *   *Note: Ensure Tesseract path is configured in `src/reader.py`.*

### Setup
1.  Clone or download this repository.
2.  Open a terminal in the project folder (`d:\Projects\Third_eye`).
3.  Install dependencies:
    ```bash
    py -m pip install -r requirements.txt
    py -m pip install kivy kivymd requests
    ```

## 🎮 Usage

### 1. Starting the AI Server (Required)
The "Brain" of the application is the Flask server. It must be running for both the Web App and Mobile App to work.

```bash
py app.py
```
*Wait for "Model loaded" and "Running on http://..." messages.*

### 2. Using the Web App
*   **PC Access**: Open `http://localhost:5000` in your browser.
*   **Mobile Access**: 
    1.  Ensure Phone and PC are on the **same Wi-Fi**.
    2.  Check the terminal for the URL (e.g., `http://192.168.1.5:5000`).
    3.  Open that URL in Chrome (Android) or Safari (iOS).
    4.  **Install**: Tap chrome menu -> "Add to Home Screen" for a full app experience.

### 3. Using the Native Mobile App (Source Code)
This runs a mobile-interface window directly on your PC.

```bash
py mobile_main.py
```
*Note: To change the server IP for the mobile app, edit `SERVER_URL` in `mobile_main.py`.*

## ⚙️ Configuration
*   **Switching Themes**: The app currently defaults to a **Premium Light** theme. You can edit `static/style.css` (Web) or `mobile_main.py` (Native) to switch back to Dark mode.
*   **Camera Source**: Defaults to webcam (Index 0). Change `cv2.VideoCapture(0)` in `app.py` or `mobile_main.py` if using an external camera.

## ❓ Troubleshooting
*   **"Camera Error"**: Ensure no other app (like Zoom or the Web App browser tab) is using the camera when launching the Native App.
*   **Mobile Not Connecting**: 
    *   Check your **Windows Firewall** (Allow Python through public/private networks).
    *   Verify both devices are on the same Wi-Fi.
    *   Use `ipconfig` to verify your PC's IP address.
*   **Gibberish Text**: Ensure lighting is good. The OCR has been tuned with confidence filtering, but blurry text is hard to read.

---
*Created by Prince | Bala*
