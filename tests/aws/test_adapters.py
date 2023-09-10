from invoicing_tools.aws.adapters import convert_pdf_to_png


def test_convert_pdf_to_png(fixtures_folder, output_folder):
    pdf_file = fixtures_folder / 'Scanned_20230514-1153.pdf'
    expected_file = output_folder / f'{pdf_file.stem}-0.png'
    expected_file.unlink(missing_ok=True)

    png_files = convert_pdf_to_png(pdf_path=pdf_file, output_path=output_folder)
    assert len(png_files) == 1
    assert png_files[0].exists()
    assert png_files[0].name == expected_file.name

    expected_file.unlink(missing_ok=True)
