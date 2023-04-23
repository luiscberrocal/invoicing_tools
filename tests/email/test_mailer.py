import os

from invoicing_tools.email.mailer import send_email
from invoicing_tools.email.models import SenderConfig, EmailMessage


def test_mail(load_environment_variables, output_folder):
    sender = SenderConfig(password=os.getenv('GMAIL_SECRET'),
                          email=os.getenv('GMAIL_USER'))
    email_message = EmailMessage(
        sender_config=sender,
        recipients=['buceo507@gmail.com'],
        attachments=[output_folder / 'processed' / 'FFiscal-CMMI-0020-20230318-0835.pdf'],
        subject='Factura Fiscal por mantenimiento Febrero 2023',
        content='Hola: Adjunto factura por mantenimiento.'
    )

    send_email(email_message)
