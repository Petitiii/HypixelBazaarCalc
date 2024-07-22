import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import re
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust the path

def preprocess_image(image):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the range of color to keep. You might need to adjust these values.
    # Example for blue text:
    lower_color = np.array([110,50,50])  # Lower range of blue
    upper_color = np.array([130,255,255])  # Upper range of blue

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)

    # Convert the result to grayscale
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to convert to binary image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Optionally resize the image to enhance readability
    resized = cv2.resize(thresh, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

    return resized

def monitor_area(region, pattern, output_file):
    last_captured = None  # To store the last captured sentence

    while True:
        screen = np.array(ImageGrab.grab(bbox=region))
        processed_image = preprocess_image(screen)

        # Using pytesseract to do OCR on the processed image
        text = pytesseract.image_to_string(processed_image)
        match = re.search(pattern, text)

        if match:
            current_match = match.group()
            if current_match != last_captured:  # Check if the current sentence is different from the last saved one
                with open(output_file, 'a') as file:
                    file.write(current_match + "\n")
                    print(current_match)  # Print the sentence for verification
                last_captured = current_match  # Update the last captured sentence

        time.sleep(2)  # Sleep to prevent excessive CPU usage

# Regex pattern for the sentence you are looking for
pattern = r"Buy Order Setup! \d+x \w+ for \d+(\.\d+)? Coins"

# Definition of the full screen area
monitor_area([0, 0, 1920, 1080], pattern, 'detected_orders.txt')
