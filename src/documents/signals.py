from django.dispatch import Signal

document_created = Signal()
document_confirmed = Signal()
document_done = Signal()
document_cancelled = Signal()