import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import re
import time

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def adjust_contrast_and_brightness(image, alpha, beta):
    # New image = alpha * original + beta
    # Alpha > 1 increases contrast
    # Beta > 0 increases brightness
    adjusted = cv2.convertScaleAbs(image, alpha=4, beta=30)
    return adjusted

def adjust_gamma(image, gamma):
   
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(image, table)

def equalize_histogram(image):
   
    # Note: Only works on grayscale images
    equalized_image = cv2.equalizeHist(image)
    return equalized_image

def adaptive_threshold(image):
    # Apply adaptive thresholding to improve text extraction
    thresholded = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)
    return thresholded
def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Adjust brightness and contrast
    brighter = adjust_contrast_and_brightness(gray, alpha=1.0, beta=50)
    
    # Apply gamma correction
    gamma_corrected = adjust_gamma(brighter, gamma=0.5)
    
    # Equalize histogram
    equalized = equalize_histogram(gamma_corrected)
    
    # Apply adaptive thresholding (optional)
    thresholded = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)
    
    return thresholded

# This routine now includes steps to enhance dark regions while preserving details.

# Ensure to define or import the helper functions adjust_contrast_and_brightness, equalize_histogram, and adaptive_threshold

def preprocess_and_save_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Save the grayscale image for inspection
    cv2.imwrite('grayscale_image.png', gray)

    # Apply binary thresholding for OCR preparation
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Optionally, resize the image to enhance readability
    resized = cv2.resize(binary, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    
    return resized

def monitor_area(region, pattern, output_file):
    last_captured = None

    while True:
        # Grab the screen region specified
        screen = np.array(ImageGrab.grab(bbox=region))
        
        # Process and save the image
        processed_image = preprocess_and_save_image(screen)

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
