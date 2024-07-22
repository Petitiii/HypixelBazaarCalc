import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract

# Konfigurieren Sie den Pfad zu Ihrem Tesseract-Executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Pfad anpassen

def monitor_area(region, target_word, output_file):
    while True:
        # Erfassen Sie einen Screenshot des spezifizierten Bereichs
        print("Monitoring")
        screen = ImageGrab.grab(bbox=region)  # x, y, Breite, Höhe
        screen_np = np.array(screen)
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

        # Verwenden Sie OCR, um Text aus dem Screenshot zu extrahieren
        text = pytesseract.image_to_string(screen_gray)

        # Prüfen Sie, ob das gesuchte Wort im Text ist
        if target_word.lower() in text.lower():
            # Speichern Sie den Text in einer Datei, wenn das Wort gefunden wird
            with open(output_file, 'a') as file:
                file.write(text + "\n")
                file.write("="*50 + "\n")  # Separator für jede Erkennung

        # Sie können hier eine kurze Pause einlegen, wenn Sie möchten
        # time.sleep(1)

# Bereich [x_start, y_start, x_end, y_end], Zielwort, Ausgabedateiname
monitor_area([333, 536,1270, 850], 'Pfad', 'detected_text.txt')