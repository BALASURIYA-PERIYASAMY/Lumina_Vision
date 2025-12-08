import pytesseract
from PIL import Image
import cv2
import numpy as np

class TextReader:
    def __init__(self, tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
    def read_text(self, image):
        """
        Reads text from a given image with confidence filtering.
        """
        try:
            # Preprocessing
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Use basic thresholding to keep it robust against different lighting
            # adaptive can sometimes add noise if parameter tuning is off
            processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            custom_config = r'--oem 3 --psm 6'
            
            # Get detailed data including confidence
            data = pytesseract.image_to_data(processed_img, config=custom_config, output_type=pytesseract.Output.DICT)
            
            valid_words = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                # Check confidence (scale 0-100)
                conf = int(data['conf'][i])
                text = data['text'][i].strip()
                
                # Filter: Confidence > 60 and Text is not empty or minimal garbage
                if conf > 60 and len(text) > 1:
                    # Optional: Strict alphanumeric check if desired
                    # if text.isalnum(): 
                    valid_words.append(text)
            
            result = " ".join(valid_words)
            return result.strip()

        except Exception as e:
            print(f"Error in OCR: {e}")
            return ""

if __name__ == "__main__":
    # Test with a dummy image if available
    pass
