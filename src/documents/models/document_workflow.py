from django.db import models


class DocumentWorkflow(models.Model):

    document_type = models.ForeignKey(
        "documents.DocumentType",
        on_delete=models.CASCADE
    )

    from_status = models.ForeignKey(
        "documents.DocumentStatus",
        on_delete=models.CASCADE,
        related_name="workflow_from"
    )

    to_status = models.ForeignKey(
        "documents.DocumentStatus",
        on_delete=models.CASCADE,
        related_name="workflow_to"
    )

    action_name = models.CharField(
        max_length=50
    )

    class Meta:
        verbose_name = "Workflow"
        verbose_name_plural = "Workflows"

    def __str__(self):
        return f"{self.document_type} {self.from_status} → {self.to_status}"