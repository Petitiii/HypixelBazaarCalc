import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import re
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Pfad anpassen

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply adaptive thresholding to enhance contrast
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Optionally resize the image to enhance readability
    resized = cv2.resize(thresh, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    return resized

def monitor_area(region, pattern, output_file):
    last_captured = None  # Zum Speichern des zuletzt erfassten Satzes

    while True:
        screen = np.array(ImageGrab.grab(bbox=region))
        processed_image = preprocess_image(screen)

        # Using pytesseract to do OCR on the processed image
        text = pytesseract.image_to_string(processed_image)
        match = re.search(pattern, text)

        if match:
            current_match = match.group()
            if current_match != last_captured:  # Überprüfe, ob der aktuelle Satz anders ist als der letzte gespeicherte
                with open(output_file, 'a') as file:
                    file.write(current_match + "\n")
                    print(current_match)  # Ausgabe des Satzes zur Überprüfung
                last_captured = current_match  # Aktualisiere den zuletzt erfassten Satz

        time.sleep(2)  # Sleep for 2 seconds to prevent excessive CPU usage

# Regex-Muster für den gesuchten Satz, der jede Art von Produkt und Menge akzeptiert
pattern = r"Buy Order Setup! \d+x \w+ for \d+(\.\d+)? Coins"

# Bereichsdefinition für den gesamten Bildschirm [x_start, y_start, x_end, y_end]
monitor_area([0, 0, 1920, 1080], pattern, 'detected_orders.txt')
