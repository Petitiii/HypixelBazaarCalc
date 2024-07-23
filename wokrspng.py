import cv2
import numpy as np
from PIL import ImageGrab, Image
import pytesseract
import re
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return binary

def extract_text_from_image(image_path, keyword):
    # Load the image from the specified path
    image = cv2.imread(image_path)
    
    # Preprocess the image to improve OCR accuracy
    processed_image = preprocess_image(image)
    
    # Perform OCR on the processed image
    text = pytesseract.image_to_string(processed_image)
    
    # Search for the keyword and capture the rest of the line
    lines = text.split('\n')
    extracted_text = ""
    for line in lines:
        if keyword in line:
            # Extract everything after the keyword
            extracted_text = line.split(keyword, 1)[1].strip()
            break
    
    return extracted_text

# Define the keyword to search for in the text
keyword = "Buy Order Setup!"

# Path to the provided image
image_path = 'testb.PNG'

# Extract text from the image
extracted_text = extract_text_from_image(image_path, keyword)

# Print the extracted text for verification
print(extracted_text)
