import os

from invoicing_tools.email.enums import EmailFormat
from invoicing_tools.email.mailer import send_email
from invoicing_tools.email.models import SenderConfig, EmailMessage


def test_mail(load_environment_variables, output_folder):
    content_file = output_folder / 'tailwind_invoice_template_email.html'
    with open(content_file, 'r') as f:
        content_template = f.read()
    recpient = os.getenv('CMMI_EMAIL')
    sender = SenderConfig(password=os.getenv('GMAIL_SECRET'),
                          email=os.getenv('GMAIL_USER'))

    filename = 'FFiscal-CMMI-0025-20230806-1245.pdf'  # FIXME
    service = 'mantenimiento de julio 2023'  # fixme
    amount = '220.00'  # fixme

    invoice_file = output_folder / 'processed' / filename
    invoice_number = int(filename.split('-')[2])
    print(f'INVOICE {invoice_number}')

    subject = f'Factura Fiscal No. {invoice_number} por {service}'
    content = content_template.format(
        invoice_number=invoice_number,
        service=service, amount=amount
    )
    email_message = EmailMessage(
        sender_config=sender,
        recipients=[recpient],
        attachments=[invoice_file],
        subject=subject,
        content=content,
        format=EmailFormat.HTML
    )

    raise Exception('xxx')  # FIXME
    response = send_email(email_message)
    print(response)
