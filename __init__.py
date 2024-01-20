#! usr/bin/env python3
import pytesseract
from PIL import Image
from PIL import ImageEnhance
image = Image.open("Reciepts/Screenshot_20240117_130009_Snapchat.jpg")

# Preprocessing the image
enhancer = ImageEnhance.Contrast(image)
enhanced_image = enhancer.enhance(2)  # Increase contrast
enhanced_image = enhanced_image.convert("L")  # Convert to grayscale

text = pytesseract.image_to_string(enhanced_image)

print(text)
