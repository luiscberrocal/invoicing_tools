from pathlib import Path
from typing import List, Optional

import pdf2image


def convert_pdf_to_png(*, pdf_path: Path, output_path: Optional[Path] = None, dpi: int = 300) -> List[Path]:
    if output_path is None:
        output_path = pdf_path.parent
    # Convert PDF pages to images
    images = pdf2image.convert_from_path(pdf_path, dpi=dpi)
    png_files = []
    # Save images as PNG files
    for i, image in enumerate(images):
        # cimage_path = f"{output_path}/page_{i + 1}.png"
        image_path = output_path / f'{pdf_path.stem}-{i}.png'
        png_files.append(image_path)
        image.save(image_path, "PNG")
    return png_files
