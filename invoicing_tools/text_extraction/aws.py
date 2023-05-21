import boto3

def extract_text_from_invoice(pdf_path):
    # Create a Textract client
    textract_client = boto3.client('textract')

    # Read the PDF file as binary data
    with open(pdf_path, 'rb') as file:
        pdf_data = file.read()

    # Start the Textract job
    response = textract_client.start_document_text_detection(Document={'Bytes': pdf_data})

    # Get the JobId
    job_id = response['JobId']

    # Wait for the job to complete
    textract_client.get_waiter('document_text_detection_completed').wait(JobId=job_id)

    # Get the response from the completed job
    response = textract_client.get_document_text_detection(JobId=job_id)

    # Extract the text from the response
    extracted_text = ""
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text += item['Text'] + '\n'

    return extracted_text

