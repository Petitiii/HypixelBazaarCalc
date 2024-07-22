import cv2
import numpy as np
from PIL import ImageGrab, ImageOps, Image
import pytesseract
import re
import time
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return binary

def monitor_area(region, pattern, output_file):

    last_captured = None

    while True:
        # Grab the screen region specified
        screen = np.array(ImageGrab.grab(bbox=region))
        
        # Preprocess the image to improve OCR accuracy
        processed_image = preprocess_image(screen)

        # Perform OCR on the processed image
        text = pytesseract.image_to_string(processed_image)
        matches = re.findall(pattern, text)

        for match in matches:
            if match != last_captured:
                with open(output_file, 'a') as file:
                    file.write(match + "\n")
                    print(match)  # Print the detected text for verification
                last_captured = match

        time.sleep(1)  # Adjust sleep time as necessary for performance vs. responsiveness

# Regular expression to match the structured sentence
pattern = r"Buy Order Setup! \d+x \w+"

# Monitor the full screen
monitor_area([0, 0, 1920, 1080], pattern, 'detected_orders.txt')
