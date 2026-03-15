import re
from django.core.exceptions import ValidationError

# -----------------------
# VALIDACIÓN PRINCIPAL
# -----------------------

def validar_identificacion(valor):
    """
    Valida una identificación ecuatoriana: cédula, RUC o pasaporte.
    """
    valor = valor.strip()

    if valor.isdigit():
        if len(valor) == 10:
            if not validar_cedula(valor):
                raise ValidationError("Cédula inválida.")
        elif len(valor) == 13:
            if not validar_ruc(valor):
                raise ValidationError("RUC inválido.")
        else:
            raise ValidationError("Número de identificación inválido.")
    else:
        # Asumimos pasaporte
        if not re.match(r'^[A-Za-z0-9]{6,15}$', valor):
            raise ValidationError("Formato de pasaporte inválido.")


# -----------------------
# VALIDACIÓN CÉDULA
# -----------------------

def validar_cedula(cedula):
    if len(cedula) != 10 or not cedula.isdigit():
        return False

    provincia = int(cedula[:2])
    if provincia < 1 or provincia > 24:
        return False

    tercer_digito = int(cedula[2])
    if tercer_digito >= 6:
        return False

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i in range(9):
        valor = int(cedula[i]) * coeficientes[i]
        if valor >= 10:
            valor -= 9
        total += valor

    verificador = 10 - (total % 10)
    if verificador == 10:
        verificador = 0

    return verificador == int(cedula[9])


# -----------------------
# VALIDACIÓN RUC
# -----------------------

def validar_ruc(ruc):
    if len(ruc) != 13 or not ruc.isdigit():
        return False

    provincia = int(ruc[:2])
    if provincia < 1 or provincia > 24:
        return False

    tercer_digito = int(ruc[2])
    if tercer_digito < 6:
        # Persona natural (usa validación de cédula)
        if not validar_cedula(ruc[:10]):
            return False
    elif tercer_digito == 6:
        # Entidad pública
        coef = [3, 2, 7, 6, 5, 4, 3, 2]
        total = sum(int(ruc[i]) * coef[i] for i in range(8))
        verificador = 11 - (total % 11)
        if verificador == 11:
            verificador = 0
        if verificador != int(ruc[8]):
            return False
    elif tercer_digito == 9:
        # Sociedad privada o extranjera
        coef = [4, 3, 2, 7, 6, 5, 4, 3, 2]
        total = sum(int(ruc[i]) * coef[i] for i in range(9))
        verificador = 11 - (total % 11)
        if verificador == 11:
            verificador = 0
        if verificador != int(ruc[9]):
            return False
    else:
        return False

    # Últimos 3 dígitos deben ser >000
    establecimiento = int(ruc[10:13])
    if establecimiento < 1:
        return False

    return True


# -----------------------
# VALIDACIÓN POR TIPO
# -----------------------

def validar_identificacion_por_tipo(valor, tipo):
    """
    Valida la identificación según el tipo seleccionado.
    """
    if not valor:
        raise ValidationError("Debe ingresar un número de identificación.")

    valor = valor.strip()

    if tipo == "CED":
        if not validar_cedula(valor):
            raise ValidationError("Cédula inválida.")
    elif tipo == "RUC":
        if not validar_ruc(valor):
            raise ValidationError("RUC inválido.")
    elif tipo == "PAS":
        if not re.match(r'^[A-Za-z0-9]{6,15}$', valor):
            raise ValidationError("Pasaporte inválido.")
    else:
        raise ValidationError("Tipo de identificación desconocido.")
