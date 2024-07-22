import cv2
import numpy as np

# Define the RGB colors
colors_rgb = {
    "orange": (251, 167, 0),
    "white": (251, 251, 251),
    "grey": (167, 167, 167),
    "green": (84, 251, 84),
    "yellow": (251, 251, 84)
}

# Convert RGB to HSV
for color_name, rgb in colors_rgb.items():
    # OpenCV uses BGR, so we need to reverse the RGB values
    rgb_bgr = np.uint8([[list(reversed(rgb))]])
    hsv = cv2.cvtColor(rgb_bgr, cv2.COLOR_BGR2HSV)
    print(f"{color_name} (HSV): {hsv[0][0]}")