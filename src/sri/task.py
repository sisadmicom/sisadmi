from celery import shared_task

from documents.models import BaseDocument

from sri.services.sri_xml_service import SriXMLService
from sri.services.sri_signature_service import SriSignatureService
from sri.services.sri_send_service import SriSendService
from sri.services.sri_pdf_service import SriPDFService
from sri.services.invoice_email_service import InvoiceEmailService


@shared_task
def process_invoice(document_id):

    document = BaseDocument.objects.get(id=document_id)

    # generar XML
    xml = SriXMLService.generate_invoice_xml(document)

    document.xml = xml.decode()
    document.save()

    # firmar XML
    signed = SriSignatureService.sign_xml(
        xml,
        "certificados/firma.p12",
        "clave_certificado"
    )

    document.xml_signed = signed.decode()
    document.save()

    # enviar al SRI
    response = SriSendService.send_xml(signed)

    document.sri_status = "ENVIADO"
    document.save()

    # consultar autorización
    auth = SriSendService.authorize(document.access_key)

    if "AUTORIZADO" in str(auth):

        document.sri_status = "AUTORIZADO"
        document.save()

        # generar PDF
        pdf = SriPDFService.generate_invoice_pdf(document)

        from django.core.files.base import ContentFile

        document.ride_pdf.save(
            f"{document.sri_number}.pdf",
            ContentFile(pdf.read())
        )

        # enviar email
        InvoiceEmailService.send_invoice(document)

"""
cuando confirmes una factura
from sri.tasks import process_invoice

process_invoice.delay(document.id)
"""

"""
ejecutar workers
en una terminal
celery -A config worker -l info
"""