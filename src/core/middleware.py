from django.utils.deprecation import MiddlewareMixin
from companies.models import Company, Branch

import threading

_user = threading.local()

def get_current_user():
    """Devuelve el usuario actual del hilo."""
    return getattr(_user, 'value', None)

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user if request.user.is_authenticated else None
        response = self.get_response(request)
        _user.value = None
        return response
    
class ActiveCompanyMiddleware(MiddlewareMixin):
    """
    Middleware para inyectar en cada request la empresa y sucursal activas
    del usuario autenticado.
    """
    def process_request(self, request):
        request.active_company = None
        request.active_branch = None

        #if not request.user.is_authenticated:
        #    return
        
        # ✅ Evita error si request.user aún no existe
        if not hasattr(request, "user") or not request.user.is_authenticated:
            return

        company_id = request.session.get("active_company_id")
        branch_id = request.session.get("active_branch_id")

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
