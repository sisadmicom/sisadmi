from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


class SriPDFService:

    @staticmethod
    def generate_invoice_pdf(document):

        buffer = BytesIO()

        pdf = canvas.Canvas(buffer, pagesize=letter)

        y = 750

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "FACTURA ELECTRÓNICA")

        y -= 30

        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, y, f"Número: {document.sri_number}")

        y -= 20
        pdf.drawString(50, y, f"Fecha: {document.date}")

        y -= 30
        pdf.drawString(50, y, f"Cliente: {document.partner.name}")

        y -= 20
        pdf.drawString(50, y, f"Identificación: {document.partner.vat}")

        y -= 40

        pdf.drawString(50, y, "Producto")
        pdf.drawString(300, y, "Cantidad")
        pdf.drawString(380, y, "Precio")
        pdf.drawString(450, y, "Total")

        y -= 20

        for line in document.lines.all():

            pdf.drawString(50, y, line.product.name)

            pdf.drawString(300, y, str(line.qty))

            pdf.drawString(380, y, str(line.price))

            pdf.drawString(450, y, str(line.subtotal))

            y -= 20
        
        y -= 20

        pdf.drawString(350, y, f"Subtotal: {document.subtotal}")

        y -= 20
        pdf.drawString(350, y, f"IVA: {document.tax_total}")

        y -= 20
        pdf.drawString(350, y, f"Total: {document.total}")

        y -= 20

        pdf.drawString(350, y, f"Subtotal: {document.subtotal}")

        y -= 20
        pdf.drawString(350, y, f"IVA: {document.tax_total}")

        y -= 20
        pdf.drawString(350, y, f"Total: {document.total}")

        pdf.save()

        buffer.seek(0)

        return buffer
"""
from django.core.files.base import ContentFile
from sri.services.sri_pdf_service import SriPDFService

pdf_buffer = SriPDFService.generate_invoice_pdf(document)

document.ride_pdf.save(
    f"{document.sri_number}.pdf",
    ContentFile(pdf_buffer.read())
)
"""