from pathlib import Path
from typing import List, Tuple

import cv2
import pytesseract
import PyPDF2
import numpy as np


def preprocess_image(image: np.ndarray) -> np.ndarray:
    # Apply preprocessing steps such as image enhancement, denoising, and thresholding
    # Return the preprocessed image
    # You can use the techniques mentioned earlier in the answer
    return image


def segment_text(image: np.ndarray) -> List[Tuple[int, int, int, int]]:
    # Perform text segmentation on the preprocessed image
    # Return a list of segmented text regions

    # Example segmentation using contour detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    text_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        text_regions.append((x, y, w, h))

    return text_regions


def extract_text_from_image(image: np.ndarray) -> str:
    # Extract text from a single image using Pytesseract OCR
    # Return the extracted text

    # Example OCR using Pytesseract
    return pytesseract.image_to_string(image)


def extract_text_from_pdf_old(pdf_path: Path) -> List[str]:
    # Extract text from a PDF file
    content = []
    # Open the PDF file
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        # Process each page in the PDF
        for page_number in range(reader.numPages):
            # Extract the page
            page = reader.getPage(page_number)
            image = page.extract_images()[0]["image"]

            # Preprocess the image
            preprocessed_image = preprocess_image(image)

            # Segment the text
            text_regions = segment_text(preprocessed_image)

            # Extract text from each region
            for region in text_regions:
                x, y, w, h = region
                region_image = preprocessed_image[y:y + h, x:x + w]
                text = extract_text_from_image(region_image)
                content.append(text)
    return content


def extract_text_from_pdf(pdf_path: Path) -> List[str]:
    # Extract text from a PDF file
    content = []
    # Open the PDF file
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        # Process each page in the PDF
        for page_number in range(len(reader.pages)):
            # Extract the page
            page = reader.pages[page_number]
            image = page.extract_images()[0]["image"]

            # Preprocess the image
            preprocessed_image = preprocess_image(image)

            # Segment the text
            text_regions = segment_text(preprocessed_image)

            # Extract text from each region
            for region in text_regions:
                x, y, w, h = region
                region_image = preprocessed_image[y:y+h, x:x+w]
                text = extract_text_from_image(region_image)
                content.append(text)
    return content
