import cv2
import numpy as np
from PIL import ImageGrab, Image
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to remove noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply thresholding to get a binary image
    _, binary = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Use dilation and erosion to remove small white noise
    kernel = np.ones((1, 1), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    
    return eroded

def extract_text_from_image(image_path, keyword):
    # Load the image from the specified path
    image = cv2.imread(image_path)
    
    # Preprocess the image to improve OCR accuracy
    processed_image = preprocess_image(image)
    
    # Perform OCR on the processed image
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    
    # Search for the keyword and capture the rest of the line
    lines = text.split('\n')
    extracted_text = ""
    for line in lines:
        if keyword in line:
            # Extract everything after the keyword
            extracted_text = line.split(keyword, 1)[1].strip()
            break
    
    return extracted_text

def capture_and_process(region, keyword, output_file):
    last_captured = None
    
    while True:
        # Capture the screen region specified
        screen = np.array(ImageGrab.grab(bbox=region))
        
        # Save the captured image to a file
        image_path = 'screenshot.png'
        cv2.imwrite(image_path, cv2.cvtColor(screen, cv2.COLOR_RGB2BGR))
        
        # Extract text from the saved image
        extracted_text = extract_text_from_image(image_path, keyword)
        
        if extracted_text and extracted_text != last_captured:
            with open(output_file, 'a') as file:
                file.write(extracted_text + "\n")
                print(extracted_text)  # Print the detected text for verification
            last_captured = extracted_text
        
        time.sleep(1)  # Adjust sleep time as necessary for performance vs. responsiveness

# Define the keyword to search for in the text
keyword = "Buy Order Setup!"

# Define the region to monitor (left, top, right, bottom)
region = (0, 0, 1920, 1080)  # Adjust this to your screen resolution or the specific area to monitor

# Output file to save detected orders
output_file = 'detected_orders.txt'

# Start capturing and processing the specified area
capture_and_process(region, keyword, output_file)
