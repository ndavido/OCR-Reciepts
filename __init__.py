#! usr/bin/env python3

from fuzzywuzzy import process
import cv2
import pytesseract
from matplotlib import pyplot as plt
import re
import numpy as np

image_path = 'Reciepts/ss.png'
image = cv2.imread(image_path)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

text = pytesseract.image_to_string(image)
filtered_text = '\n'.join(
    line for line in text.split('\n') if line.strip() != '')

print(filtered_text)


def extract_receipt_info_single(receipt_text):
    # Convert all text to lowercase to simplify matching
    text_lower = receipt_text.lower()

    # Initialize the result dictionary
    info = {
        'fuel_type': None,
        'volume': None,
        'price_per_litre': None,
        'total': None
    }

    # https://stackoverflow.com/questions/1547574/regex-for-prices
    volume_pattern = r"(?i)(?:volume|;|:|diesel|unleaded|pump\s*([a-z]|[0-9])|\))\s*(\d+(?:[.,]\d{2}))\s*°?\s*(ltr|l|net)?"

    price_per_litre_pattern = r"(?:price|€)\s*([1-9][.,]\d{3})\s*(eur/l|/l|/)?\s*"

    # Define fuel type choices for fuzzy matching
    fuel_type_choices = ["unleaded", "diesel"]

    # Search for fuel type with fuzzy match
    fuel_type_match = process.extractOne(
        text_lower, fuel_type_choices, score_cutoff=50)
    if fuel_type_match:
        info['fuel_type'] = fuel_type_match[0]

    # Search for volume
    volume_match = re.search(volume_pattern, text_lower)
    if volume_match:
        info['volume'] = next((m for m in volume_match.groups() if m), None)
        if info['volume'] is not None:
            info['volume'] = info['volume'].replace(',', '.')

    # Search for price per litre
    price_per_litre_match = re.search(price_per_litre_pattern, text_lower)
    if price_per_litre_match:
        info['price_per_litre'] = next(
            (m for m in price_per_litre_match.groups() if m), None)
        if info['price_per_litre'] is not None:
            info['price_per_litre'] = info['price_per_litre'].replace(',', '.')

    if info['volume'] is not None and info['price_per_litre'] is not None:
        total = float(info['volume']) * float(info['price_per_litre'])
        total = round(total, 2)
        info['total'] = total
    else:
        info['total'] = None

    return info


extracted_info_single = extract_receipt_info_single(filtered_text)
print(extracted_info_single)
