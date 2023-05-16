from invoicing_tools.text_extraction.aws import extract_text_from_invoice


def test_textextract(fixtures_folder):
    # Usage
    f = fixtures_folder / 'Scanned_20230514-1153.pdf'
    extracted_text = extract_text_from_invoice(f)
    print(extracted_text)
