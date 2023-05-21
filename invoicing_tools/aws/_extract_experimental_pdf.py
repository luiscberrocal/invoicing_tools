from pathlib import Path

import boto3
from PIL import Image, ImageDraw
import io
import json
import textract
from typing import Dict, Any

from invoicing_tools.aws.config import read_credentials_from_json


def draw_bounding_box(key: str, val: Dict[str, Any], width: int, height: int, draw: ImageDraw.Draw) -> None:
    # If a key is Geometry, draw the bounding box info in it
    if "Geometry" in key:
        # Draw bounding box information
        box = val["BoundingBox"]
        left = width * box['Left']
        top = height * box['Top']
        draw.rectangle([left, top, left + (width * box['Width']), top + (height * box['Height'])],
                       outline='black')

# Takes a field as an argument and prints out the detected labels and values
def print_labels_and_values(field: Dict[str, Any]) -> None:
    # Only if labels are detected and returned
    if "LabelDetection" in field:
        print("Summary Label Detection - Confidence: {}".format(
            str(field.get("LabelDetection")["Confidence"])) + ", "
              + "Summary Values: {}".format(str(field.get("LabelDetection")["Text"])))
    else:
        print("Label Detection - No labels returned.")
    if "ValueDetection" in field:
        print("Summary Value Detection - Confidence: {}".format(
            str(field.get("ValueDetection")["Confidence"])) + ", "
              + "Summary Values: {}".format(str(field.get("ValueDetection")["Text"])))
    else:
        print("Value Detection - No values returned")

def process_text_detection(bucket: str, document: str, access_key: str, secret_key: str,
                           folder: Path) -> Dict[str, Any]:
    # Get the document from S3
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3_response = s3.get_object(Bucket=bucket, Key=document)

    # Check if the document is a PDF
    if document.lower().endswith('.pdf'):
        # Extract text from the PDF using textract
        pdf_content = s3_response['Body'].read()
        text = textract.process(io.BytesIO(pdf_content))
        response = json.loads(text)
    else:
        # Open binary stream using an in-memory bytes buffer
        stream = io.BytesIO(s3_response['Body'].read())

        # Load stream into image
        image = Image.open(stream)

        # Detect text in the document
        textract = boto3.client('textract', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name="us-east-2")
        response = textract.analyze_expense(Document={'S3Object': {'Bucket': bucket, 'Name': document}})

        # Set width and height to display image and draw bounding boxes
        # Create drawing object
        width, height = image.size
        draw = ImageDraw.Draw(image)

        for expense_doc in response["ExpenseDocuments"]:
            for line_item_group in expense_doc["LineItemGroups"]:
                for line_items in line_item_group["LineItems"]:
                    for expense_fields in line_items["LineItemExpenseFields"]:
                        print_labels_and_values(expense_fields)
                        print()

            print("Summary:")
            for summary_field in expense_doc["SummaryFields"]:
                print_labels_and_values(summary_field)
                print()

            # For draw bounding boxes
            for line_item_group in expense_doc["LineItemGroups"]:
                for line_items in line_item_group["LineItems"]:
                    for expense_fields in line_items["LineItemExpenseFields"]:
                        for key, val in expense_fields["ValueDetection"].items():
                            if "Geometry" in key:
                                draw_bounding_box(key, val, width, height, draw)

            for label in expense_doc["SummaryFields"]:
                if "LabelDetection" in label:
                    for key, val in label["LabelDetection"].items():
                        draw_bounding_box(key, val, width, height, draw)

        # Display the image
        image.save(folder / document)

    return response
def extract():
    library_folder = Path(__file__).parent.parent.parent
    envs_folder = library_folder / '.envs'
    output_folder = library_folder / 'output'

    json_file_path = envs_folder / 'invoice-user-aws-config.json'  # Path to the JSON file containing access key and secret key
    access_key, secret_key, bucket = read_credentials_from_json(json_file_path)
    document = 'Scanned_20230514-1153.pdf'

    response = process_text_detection(bucket=bucket, document=document, access_key=access_key, secret_key=secret_key,
                                      folder=output_folder)
    print(response)


if __name__ == '__main__':
    extract()
