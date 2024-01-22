#! usr/bin/env python3

import cv2
import pytesseract
from matplotlib import pyplot as plt

# Load the image from the file system
# image_path = 'Reciepts/20240121_123406.jpg'
image_path = 'Reciepts/Screenshot_20240119_144636_Snapchat.jpg'
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(
    gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Perform OCR on the preprocessed image
text = pytesseract.image_to_string(binary_image)

# Define a function to parse the OCR results


def parse_fuel_receipt(ocr_text):
    # Initialize variables
    fuel_type = None
    price_per_litre = None
    total_cost = None

    # Iterate through each line of OCR text
    for line in ocr_text.split('\n'):
        # Check if the line contains the fuel type
        if 'diesel' in line.lower():
            fuel_type = 'Diesel'
        elif 'unleaded' in line.lower():
            fuel_type = 'Unleaded'

        # Try to find the price per litre
        if '€' in line and '/' in line:
            parts = line.split()
            for part in parts:
                if '€' in part:
                    price_per_litre = part

        # Try to find the total cost
        if 'total' in line.lower():
            total_cost = line.split('€')[-1].strip()

    return fuel_type, price_per_litre, total_cost


# Parse the OCR results
fuel_type, price_per_litre, total_cost = parse_fuel_receipt(text)

# Print the results
print(f"Fuel Type: {fuel_type}")
print(f"Price per Litre: {price_per_litre}")
print(f"Total Cost: {total_cost}")
