import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import re
import time

# Configure the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply a binary threshold to the image
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Optionally, resize the image to enhance readability
    resized = cv2.resize(binary, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

    return resized

def monitor_area(region, pattern, output_file):
    last_captured = None

    while True:
        screen = np.array(ImageGrab.grab(bbox=region))
        processed_image = preprocess_image(screen)

        # Perform OCR on the processed image
        text = pytesseract.image_to_string(processed_image)
        match = re.search(pattern, text)

        if match:
            current_match = match.group()
            if current_match != last_captured:
                with open(output_file, 'a') as file:
                    file.write(current_match + "\n")
                    print(current_match)  # Print the detected text for verification
                last_captured = current_match

        time.sleep(2)  # Pause to reduce CPU usage

# Regular expression to match the structured sentence
pattern = r"Buy Order Setup! \d+x \w+ for \d+(\.\d+)? Coins"

# Monitor the full screen
monitor_area([0, 0, 1920, 1080], pattern, 'detected_orders.txt')
