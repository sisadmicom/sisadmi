from django.core.mail import EmailMessage


class InvoiceEmailService:

    @staticmethod
    def send_invoice(document):

        subject = f"Factura Electrónica {document.sri_number}"

        body = f"""
Estimado {document.partner.name},

Adjunto encontrará su factura electrónica.

Número: {document.sri_number}
Total: {document.total}

Gracias por su compra.
"""

        email = EmailMessage(
            subject,
            body,
            to=[document.partner.email]
        )

from django.core.mail import EmailMessage


class InvoiceEmailService:

    @staticmethod
    def send_invoice(document):

        subject = f"Factura Electrónica {document.sri_number}"

        body = f"""
Estimado {document.partner.name},

Adjunto encontrará su factura electrónica.

Número: {document.sri_number}
Total: {document.total}

Gracias por su compra.
"""

        email = EmailMessage(
            subject,
            body,
            to=[document.partner.email]
        )

"""
Enviar automaticamente cuando el sri autoricw
from sri.services.invoice_email_service import InvoiceEmailService

InvoiceEmailService.send_invoice(document)
""" 