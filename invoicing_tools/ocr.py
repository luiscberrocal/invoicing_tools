from pathlib import Path

import pytesseract


def ocr_file(filename: Path) -> str:
    string_value = pytesseract.image_to_string(str(filename))
    return string_value.replace('\n', ' ')


if __name__ == '__main__':
    file = Path('../output/tag2.jpg')
    print(file.exists())
    scanned = ocr_file(file)
    print(scanned)

    file = Path('../output/tag1.jpg')
    print(file.exists())
    scanned = ocr_file(file)
    print(scanned)

    file = Path('../output/tag3.jpg')
    print(file.exists())
    scanned = ocr_file(file)
    print(scanned)
