import json
from pathlib import Path
from typing import Optional

from invoicing_tools.aws.adapters import convert_pdf_to_png
from invoicing_tools.aws.config import read_credentials_from_json
from invoicing_tools.aws.extraction import process_text_detection
from invoicing_tools.aws.s3_management import upload_file_to_s3
from invoicing_tools.exceptions import ConversionError


def process_local_pdf_receipt(*, pdf_file: Path, configuration_file: Path, output_folder: Optional[Path] = None):
    # Converts pdf to png
    png_files = convert_pdf_to_png(pdf_path=pdf_file)
    if len(png_files) > 1:
        ConversionError('Multi page receipts are not supported yet.')
    if output_folder is None:
        output_folder = pdf_file.parent

    access_key, secret_key, bucket = read_credentials_from_json(configuration_file)

    # Uploads to S3
    file_to_upload = png_files[0]
    upload_file_to_s3(file_path=file_to_upload, bucket_name=bucket, access_key=access_key, secret_key=secret_key)

    response = process_text_detection(bucket=bucket, document=file_to_upload.name,
                                      access_key=access_key, secret_key=secret_key,
                                      folder=output_folder)

    json_response_file = output_folder / f'{pdf_file.stem}.json'

    with open(json_response_file, 'w') as f:
        json.dump(response, f, indent=4)


if __name__ == '__main__':
    library_folder = Path(__file__).parent.parent.parent

    envs_folder = library_folder / '.envs'
    output_dir = library_folder / 'output'

    json_file_path = envs_folder / 'invoice-user-aws-config.json'  # Path to the JSON file containing access key and secret key
    document = 'Scanned_20230521-1544.pdf'
    pdf = output_dir / document
    process_local_pdf_receipt(pdf_file=pdf, configuration_file=json_file_path)
