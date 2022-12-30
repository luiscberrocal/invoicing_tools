from invoicing_tools.ocr import ocr_file


def test_read_jpeg(output_folder, fixtures_folder):
    file = output_folder / 'tag1.jpg'
    scanned = ocr_file(file)
    print(scanned)


def test_read_pdf(output_folder, fixtures_folder):
    file = output_folder / 'Fact-007_20220329-1811.pdf'
    scanned = ocr_file(file)
    print(scanned)
