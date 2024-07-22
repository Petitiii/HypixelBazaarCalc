import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import re


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Pfad anpassen

def monitor_area(region, pattern, output_file):
    while True:
        
        screen = ImageGrab.grab(bbox=region)  
        screen_np = np.array(screen)
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

        
        text = pytesseract.image_to_string(screen_gray)
        match = re.search(pattern, text)
        if match:
            with open(output_file, 'a') as file:
                file.write(match.group() + "\n")  # Speicher den Satz
                print(match.group())

       
        # time.sleep(1)

# Regex-Muster für den gesuchten Satz, der jede Art von Produkt und Menge akzeptiert
pattern = r"Your Buy Order Setup! \d+x \w+ for \d+(\.\d+)? Coins"

# [x_start, y_start, x_end, y_end], Regex-Muster
monitor_area([333, 536,1270, 850], pattern, 'detected_orders.txt')
