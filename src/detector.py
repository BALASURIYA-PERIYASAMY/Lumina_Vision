from ultralytics import YOLO
import cv2

class ObjectDetector:
    def __init__(self, model_path='yolov8m.pt'):
        try:
            print(f"Loading YOLO model: {model_path}...")
            self.model = YOLO(model_path)
            print("Model loaded.")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            self.model = None

    def detect(self, image):
        """
        Detects objects in the image.
        Returns a list of dictionaries with 'label' and 'confidence'.
        """
        if self.model is None:
            return []

        results = self.model(image, verbose=False)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.model.names[cls_id]
                
                # Filter low confidence if needed (YOLO usually filters by default conf threshold)
                if conf > 0.5:
                    detections.append({'label': label, 'confidence': conf})
        
        return detections

    def describe_scene(self, detections):
        """
        Converts detections into a natural language string.
        """
        if not detections:
            return "I don't see anything recognizable."
        
        # Count objects
        counts = {}
        for d in detections:
            label = d['label']
            counts[label] = counts.get(label, 0) + 1
            
        description_parts = []
        for label, count in counts.items():
            if count == 1:
                description_parts.append(f"a {label}")
            else:
                description_parts.append(f"{count} {label}s")
                
        scene_desc = "I see " + ", ".join(description_parts) + "."
        return scene_desc

if __name__ == "__main__":
    detector = ObjectDetector()
    # Test would go here
