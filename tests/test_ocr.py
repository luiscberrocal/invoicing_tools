from pdf2image import convert_from_path

from invoicing_tools.ocr import ocr_file, ocr_lines, ocr_pdf_file, ocr_pdfs_in_folder, read_pdf


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


def test_ocr_pdf(output_folder):
    file = output_folder / 'Fact-007_20220329-1811.pdf'
    jpg_file = output_folder / 'Fact-007_20220329-1811.jpg'
    txt_file = output_folder / 'Fact-007_20220329-1811.txt'
    jpg_file.unlink(missing_ok=True)

    lines = ocr_pdf_file(file)
    with open(txt_file, 'w') as txt:
        for i, line in enumerate(lines):
            print(f'>> {i} {line}')
            txt.write(f'{line}\n')


def test_ocr_pdf_multiple(output_folder):
    folder = output_folder / 'invoices_to_process'
    ocr_pdfs_in_folder(folder)


def test_read_pdf(output_folder):
    f = output_folder / 'Scanned_20230514-1153.pdf'
    content = read_pdf(f)
    for c in content:
        print(c)

