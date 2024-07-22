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

def monitor_area(region, keyword, output_file):

    last_captured = None

    while True:
        # Grab the screen region specified
        screen = np.array(ImageGrab.grab(bbox=region))
        
        # Preprocess the image to improve OCR accuracy
        processed_image = preprocess_image(screen)

        # Perform OCR on the processed image
        text = pytesseract.image_to_string(processed_image)

        # Search for the keyword and capture the rest of the line
        lines = text.split('\n')
        for line in lines:
            if keyword in line:
                # Extract everything after the keyword
                extracted_text = line.split(keyword, 1)[1].strip()
                if extracted_text != last_captured:
                    with open(output_file, 'a') as file:
                        file.write(extracted_text + "\n")
                        print(extracted_text)  # Print the detected text for verification
                    last_captured = extracted_text

        time.sleep(1)  # Adjust sleep time as necessary for performance vs. responsiveness

# Keyword to search for in the text
keyword = "Buy Order Setup!"

# Monitor the full screen
monitor_area([0, 0, 1920, 1080], keyword, 'detected_orders.txt')
