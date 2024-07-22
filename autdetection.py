import cv2
import numpy as np
from PIL import ImageGrab, ImageOps, Image
import pytesseract
import re
import time

# Configure the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    """Process image for OCR by converting it to grayscale, inverting, and thresholding."""
    # Convert image to grayscale
    img = Image.fromarray(image).convert("L")
    
    # Invert image colors
    img = ImageOps.invert(img)
    
    # Apply binary thresholding
    np_image = np.array(img)
    thresh = 240
    binary_image = (np_image > thresh) * 255  # Binary thresholding simplified
    return Image.fromarray(np.uint8(binary_image))

def monitor_area(region, pattern, output_file):
    """Monitor specified screen region for changes and perform OCR."""
    last_captured = None

    while True:
        # Grab the screen region specified
        screen = np.array(ImageGrab.grab(bbox=region))
        
        # Process the image
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

        time.sleep(1)  # Adjust sleep time as necessary for performance vs. responsiveness

# Regular expression to match the structured sentence
pattern = r"Buy Order Setup! \d+x \w+ for \d+(\.\d+)? Coins"

# Monitor the full screen
monitor_area([0, 0, 1920, 1080], pattern, 'detected_orders.txt')
