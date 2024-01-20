#! usr/bin/env python3
import pytesseract
from PIL import Image
from PIL import ImageEnhance, ImageFilter
import numpy as np
import cv2


def preprocess_image(image_path):
    # Open the image
    image = Image.open(image_path)

    # Convert image to grayscale
    image = image.convert('L')

    # Enhance the image
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)

    # Convert image to an array for further processing
    image_np = np.array(image)

    # Deskew (correct tilt) the image
    coords = np.column_stack(np.where(image_np > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image_np.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    image_np = cv2.warpAffine(
        image_np, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Convert back to PIL image
    processed_image = Image.fromarray(image_np)

    return processed_image


def extract_text_from_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(preprocessed_image)
    return text


image_path = "Reciepts/image0.jpg"
text = extract_text_from_image(image_path)
print(text)
