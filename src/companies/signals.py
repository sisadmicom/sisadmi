# companies/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from companies.models import Company, Branch

@receiver(user_logged_in)
def assign_default_company_branch(sender, user, request, **kwargs):
    """
    Asigna automáticamente la empresa y sucursal activa al usuario cuando inicia sesión.
    """
    company = Company.objects.first()
    branch = Branch.objects.filter(company=company).first()

    if company and branch:
        # Guardamos en la sesión
        request.session['active_company_id'] = company.id
        request.session['active_branch_id'] = branch.id
        print(f"✅ {user.username} usando {company.name} / {branch.name}")
