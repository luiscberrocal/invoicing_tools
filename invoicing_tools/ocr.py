import logging
from pathlib import Path
from time import time
from typing import List
import numpy as np
import cv2
import pytesseract
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)


def ocr_file(filename: Path) -> str:
    string_value = pytesseract.image_to_string(str(filename))
    return string_value.replace('\n', ' ')


def ocr_lines(filename: Path) -> List[str]:
    string_value = pytesseract.image_to_string(str(filename))
    return string_value.split('\n')


def ocr_pdf_file(pdf_file: Path, dpi: int = 600, multi_paged: bool = False) -> List[str]:
    pdf_pages = convert_from_path(pdf_file, dpi)
    jpeg_file = pdf_file.parent / f'{pdf_file.stem}.jpg'
    if multi_paged:
        raise Exception('Not supported yet')
    pdf_pages[0].save(jpeg_file, 'JPEG')
    scanned = ocr_lines(jpeg_file)
    logger.debug(f'Converted pdf to jpeg {jpeg_file}')
    return scanned


def ocr_pdfs_in_folder(folder: Path) -> List[Path]:
    start = time()
    pdf_files = folder.glob('**/*.pdf')
    txt_files = list()
    for pdf_file in pdf_files:
        lines = ocr_pdf_file(pdf_file)
        txt_file = folder / f'{pdf_file.stem}.txt'
        with open(txt_file, 'w') as txt:
            for i, line in enumerate(lines):
                txt.write(f'{line}\n')
        txt_files.append(txt_file)
    elapsed = time() - start
    per_file = elapsed / len(txt_files)
    logger.debug(f'Processed {len(txt_files)} pdf files in {elapsed:.2f} seconds ({per_file:.2f} seconds per file)')
    return txt_files


def read_pdf(pdf_file: Path, dpi: int = 600) -> List[str]:
    """Suggestion by ChatGPT"""
    content = []
    # Load the PDF image and convert it to a list of PIL images
    pages = convert_from_path(pdf_file, dpi)

    # Loop over each PIL image and process it
    for i, page in enumerate(pages):
        # Convert the PIL image to a numpy array
        img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        # Apply some image processing to enhance the text
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Perform OCR on the image using pytesseract
        text = pytesseract.image_to_string(gray)

        # Print the OCR results
        #  print(f"Page {i + 1} OCR Text:\n{text}")
        content.append(text)
    return content
