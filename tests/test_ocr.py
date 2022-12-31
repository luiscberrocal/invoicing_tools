from pdf2image import convert_from_path

from invoicing_tools.ocr import ocr_file, ocr_lines


def test_read_jpeg(output_folder, fixtures_folder):
    file = output_folder / 'tag1.jpg'
    scanned = ocr_file(file)
    print(scanned)


def test_read_pdf(output_folder, fixtures_folder):
    file = output_folder / 'Fact-007_20220329-1811.pdf'
    jpg_file = output_folder / 'Fact-007_20220329-1811.jpg'
    pdf_pages = convert_from_path(file, 500)
    assert len(pdf_pages) == 1
    pdf_pages[0].save(jpg_file, 'JPEG')
    scanned = ocr_lines(jpg_file)
    print(scanned)
