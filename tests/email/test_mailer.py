import os

from invoicing_tools.email.enums import EmailFormat
from invoicing_tools.email.mailer import send_email
from invoicing_tools.email.models import SenderConfig, EmailMessage


def test_mail(load_environment_variables, output_folder):
    content_file = output_folder / 'tailwind_invoice_template_email.html'
    with open(content_file, 'r') as f:
        content = f.read()

    content2 = """\
    <html>
      <head></head>
      <body>
        <h3>Factura Fiscal</h3>
        <p>Hola!<br>
           How are you?<br>
           Here is the <a href="http://www.python.org">link</a> you wanted.
        </p>
      </body>
    </html>
    """
    sender = SenderConfig(password=os.getenv('GMAIL_SECRET'),
                          email=os.getenv('GMAIL_USER'))

    invoice_file = output_folder / 'processed' / 'FFiscal-CMMI-0020-20230318-0835.pdf'
    subject = 'Factura Fiscal No. 20 por mantenimiento Febrero 2023 x $210.00'

    invoice_file = output_folder / 'processed' / 'FFiscal-CMMI-0019-20230218-0832.pdf'
    subject = 'Factura Fiscal No. 19 por mantenimiento de Enero 2023'

    email_message = EmailMessage(
        sender_config=sender,
        recipients=['buceo507@gmail.com'],
        attachments=[invoice_file],
        subject=subject,
        content=content,
        format=EmailFormat.HTML
    )

    response = send_email(email_message)
    print(response)
