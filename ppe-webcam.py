from config import IMAGE_DIR  # Assuming you still want to save some images
import os
import cv2
import time
import logging
from ultralytics import YOLO  # Ensure this is the correct import for your YOLO model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load your YOLO model
model = YOLO("best.pt")
classNames = ['Hardhat', 'NO-Hardhat', 'Person']
class_settings = {
    'NO-Hardhat':     ((0, 0, 255), True, False),
    'Hardhat':        ((0, 255, 0), False, False),
    'Person':         ((255, 0, 0), False, True)
}
# Default settings for classes not listed above
default_settings = ((255, 0, 0), False, False)

def process_frame(img):
    detected_items = set()
    has_person = False

    results = model(img, stream=True)
    for box in [box for r in results for box in r.boxes if box.conf[0] > 0.5]:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls = int(box.cls[0])
        currentClass = classNames[cls]
        logging.info(currentClass)

        detected_items.add(currentClass)  # Add detected item to the set

        color, _, person = class_settings.get(currentClass, default_settings)
        cv2.putText(img, f'{classNames[cls]}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
        has_person = has_person or person

    # Check for violations based on the presence or absence of specific items
    mandatory_items = {'Hardhat'}
    no_items = {'NO-Hardhat'}
    has_mandatory_items = mandatory_items.issubset(detected_items)
    has_no_items = not no_items.isdisjoint(detected_items)

    has_violation = has_no_items and not has_mandatory_items

    if has_violation and has_person:
        timestamp = str(time.time())
        filename = os.path.join(IMAGE_DIR, f"{timestamp}.jpg")
        cv2.imwrite(filename, img)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # 0 is typically the default camera

    while True:
        success, img = cap.read()
        if not success:
            break

        process_frame(img)

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()