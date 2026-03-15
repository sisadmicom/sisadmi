from companies.models import Company, Branch

class CompanyContextMiddleware:
    """Guarda en la request la empresa y sucursal activas del usuario."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        company_id = request.session.get("active_company")
        branch_id = request.session.get("active_branch")

        request.active_company = None
        request.active_branch = None

        if company_id:
            try:
                request.active_company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                pass

        if branch_id:
            try:
                request.active_branch = Branch.objects.get(id=branch_id)
            except Branch.DoesNotExist:
                pass

        return self.get_response(request)
