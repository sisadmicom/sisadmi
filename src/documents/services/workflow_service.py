from documents.models import DocumentWorkflow

class WorkflowService:

    @staticmethod
    def change_status(document, action):

        workflow = DocumentWorkflow.objects.filter(
            document_type=document.document_type,
            from_status=document.status,
            action_name=action
        ).first()

        if not workflow:
            raise Exception("Acción no permitida")

        document.status = workflow.to_status
        document.save()

        # emitir eventos
        if workflow.to_status.code == "confirmed":
            document_confirmed.send(sender=document.__class__, document=document)

        if workflow.to_status.code == "done":
            document_done.send(sender=document.__class__, document=document)

        if workflow.to_status.code == "cancelled":
            document_cancelled.send(sender=document.__class__, document=document)

        return document
"""class WorkflowService:

    @staticmethod
    def change_status(document, action):

        workflow = DocumentWorkflow.objects.filter(
            document_type=document.document_type,
            from_status=document.status,
            action_name=action
        ).first()

        if not workflow:
            raise Exception("Acción no permitida")

        document.status = workflow.to_status
        document.save()

        return document

from documents.signals import (
    document_confirmed,
    document_done,
    document_cancelled
)
"""