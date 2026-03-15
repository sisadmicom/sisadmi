from django.db import transaction

from documents.models import (
    BaseDocument,
    BaseDocumentLine,
    DocumentSettings,
)


class DocumentService:

    @staticmethod
    @transaction.atomic
    def create_document(
        document_type,
        partner=None,
        date=None,
        lines=None
    ):
        """
        Crea un documento completo con numeración y líneas
        """

        settings = document_type.documentsettings

        sequence = settings.sequence
        number = sequence.next()

        document = BaseDocument.objects.create(
            document_type=document_type,
            number=number,
            status=settings.initial_status,
            partner=partner,
            date=date
        )

        total = 0

        if lines:
            for line in lines:

                qty = line["qty"]
                price = line["price"]

                subtotal = qty * price

                BaseDocumentLine.objects.create(
                    document=document,
                    product=line["product"],
                    qty=qty,
                    price=price,
                    subtotal=subtotal
                )

                total += subtotal

        document.total = total
        document.save()

        return document