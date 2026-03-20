from django.dispatch import receiver

from documents.signals import document_confirmed


@receiver(document_confirmed)
def create_inventory_move(sender, document, **kwargs):

    if document.document_type.code != "sale_order":
        return

    print("Crear movimiento de inventario")