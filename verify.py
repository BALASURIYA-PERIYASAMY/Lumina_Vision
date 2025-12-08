from src.speaker import Speaker
from src.detector import ObjectDetector
from src.reader import TextReader
import cv2
import numpy as np

def test_speaker():
    print("Testing Speaker...")
    s = Speaker()
    s.speak("Testing speaker system.")

def test_detector():
    print("Testing Detector (Model Load)...")
    d = ObjectDetector() # Will download model if not present
    if d.model:
        print("Detector loaded successfully.")
    else:
        print("Detector failed to load.")

def test_reader():
    print("Testing Reader...")
    r = TextReader()
    # Create a blank image with text
    img = np.zeros((100, 300, 3), dtype=np.uint8)
    cv2.putText(img, 'TEST', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    text = r.read_text(img)
    print(f"OCR Output: {text}")

if __name__ == "__main__":
    test_speaker()
    test_detector()
    test_reader()
