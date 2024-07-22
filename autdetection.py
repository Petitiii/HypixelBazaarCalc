import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import re
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Pfad anpassen

def monitor_area(region, pattern, output_file):
    last_captured = None  # Zum Speichern des zuletzt erfassten Satzes

    while True:
        screen = ImageGrab.grab(bbox=region)
        screen_np = np.array(screen)
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(screen_gray)
        match = re.search(pattern, text)

        if match:
            current_match = match.group()
            if current_match != last_captured:  # Überprüfe, ob der aktuelle Satz anders ist als der letzte gespeicherte
                with open(output_file, 'a') as file:
                    file.write(current_match + "\n")
                    print(current_match)  # Ausgabe des Satzes zur Überprüfung
                last_captured = current_match  # Aktualisiere den zuletzt erfassten Satz

        time.sleep(2)  

# Regex-Muster für den gesuchten Satz, der jede Art von Produkt und Menge akzeptiert
pattern = r"Your Buy Order Setup! \d+x \w+ for \d+(\.\d+)? Coins"

# Bereichsdefinition [x_start, y_start, x_end, y_end]
monitor_area([333, 536, 1270, 850], pattern, 'detected_orders.txt')
