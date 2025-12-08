import cv2
import sys
import os
import time
# Add project root to path to ensure imports work if run from different locations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.speaker import Speaker
from src.detector import ObjectDetector
from src.reader import TextReader

def interactive_mode():
    print("Initializing Third Eye modules...")
    speaker = Speaker()
    speaker.speak("Initializing Third Eye.")
    
    try:
        detector = ObjectDetector()
        reader = TextReader() 
    except Exception as e:
        print(f"Error initializing modules: {e}")
        return

    print("Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        speaker.speak("Error. Could not open camera.")
        return

    speaker.speak("Camera ready. Press 'd' for description, 'r' to read text, 'q' to quit.")
    print("Controls: 'd' = Describe Scene, 'r' = Read Text, 'q' = Quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow('Third Eye View', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('d'):
            speaker.speak("Analyzing scene...")
            detections = detector.detect(frame)
            description = detector.describe_scene(detections)
            print(f"Scene: {description}")
            speaker.speak(description)
        elif key == ord('r'):
            speaker.speak("Reading text...")
            text = reader.read_text(frame)
            if text:
                print(f"Text detected: {text}")
                speaker.speak(f"Text says: {text}")
            else:
                print("No text detected.")
                speaker.speak("No text detected.")

    cap.release()
    cv2.destroyAllWindows()
    speaker.speak("Goodbye.")

def file_mode(image_path, mode):
    speaker = Speaker()
    detector = ObjectDetector()
    reader = TextReader()
    
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return

    if mode == 'detect':
        detections = detector.detect(img)
        description = detector.describe_scene(detections)
        print(f"Scene: {description}")
        speaker.speak(description)
    elif mode == 'read':
        text = reader.read_text(img)
        if text:
            print(f"Text detected: {text}")
            speaker.speak(f"Text says: {text}")
        else:
            print("No text detected.")
            speaker.speak("No text detected.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # File mode usage: python main.py <image_path> <mode: detect/read>
        if len(sys.argv) >= 3:
            file_mode(sys.argv[1], sys.argv[2])
        else:
            print("Usage: python src/main.py <image_path> <detect|read>")
    else:
        interactive_mode()
