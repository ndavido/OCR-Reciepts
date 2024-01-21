#! usr/bin/env python3

import cv2
import pytesseract

image_path = 'Reciepts/20240121_123406.jpg'
image = cv2.imread(image_path)

text = pytesseract.image_to_string(image)

# Remove multiple empty lines
filtered_text = '\n'.join(
    line for line in text.split('\n') if line.strip() != '')

print(filtered_text)
