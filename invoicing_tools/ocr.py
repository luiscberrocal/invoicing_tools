from pathlib import Path
from typing import List

import pytesseract
from pdf2image import convert_from_path


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
    return scanned


def ocr_pdfs_in_folder(folder: Path):
    pdf_files = folder.glob('**/*.pdf')
    for pdf_file in pdf_files:
        lines = ocr_pdf_file(pdf_file)
        txt_file = folder / f'{pdf_file.stem}.txt'
        with open(txt_file, 'w') as txt:
            for i, line in enumerate(lines):
                txt.write(f'{line}\n')
