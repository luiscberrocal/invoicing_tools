from invoicing_tools.text_extraction.segmentation import extract_text_from_pdf


def test_read_pdf(fixtures_folder):
    f = fixtures_folder / 'Scanned_20230514-1153.pdf'
    content = extract_text_from_pdf(f)
    for c in content:
        print(c)
