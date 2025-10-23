from django.contrib import admin

class CompanyFilteredAdmin(admin.ModelAdmin):
    """Base admin que filtra por empresa y sucursal activas."""

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(qs.model, "company") and request.active_company:
            qs = qs.filter(company=request.active_company)
        if hasattr(qs.model, "branch") and request.active_branch:
            qs = qs.filter(branch=request.active_branch)
        return qs

    def save_model(self, request, obj, form, change):
        # Asigna automáticamente la empresa/sucursal activa al guardar
        if hasattr(obj, "company") and not obj.company:
            obj.company = request.active_company
        if hasattr(obj, "branch") and not obj.branch:
            obj.branch = request.active_branch
        super().save_model(request, obj, form, change)
