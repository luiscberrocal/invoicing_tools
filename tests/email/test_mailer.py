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

    # filename = 'FFiscal-CMMI-0017-20221203-1052.pdf'
    # invoice_file = output_folder / 'processed' / filename
    # invoice_number = int(filename.split('-')[2])
    # service = 'mantenimiento de Diciembre 2022'
    # amount = '200.00'

    # filename = 'FFiscal-CMMI-0020-20230318-0835.pdf'

    # invoice_file = output_folder / 'processed' / filename
    # invoice_number = int(filename.split('-')[2])
    # service = 'mantenimiento de Febrero 2023'
    # amount = '210.00'
    # print(f'INVOICE {invoice_number}')
    # raise Exception('xxx')
    # invoice_file = output_folder / 'processed' / 'FFiscal-CMMI-0019-20230218-0832.pdf'
    # invoice_number = 19
    # service = 'mantenimiento de Enero 2023'
    # amount = '200.00'

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

    response = send_email(email_message)
    print(response)
