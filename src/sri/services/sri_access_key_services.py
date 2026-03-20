import random


class SriAccessKeyService:

    @staticmethod
    def generate_access_key(
        date,
        document_type,
        ruc,
        environment,
        establishment,
        emission_point,
        sequential,
        emission_type="1"
    ):

        date_str = date.strftime("%d%m%Y")

        serie = f"{establishment}{emission_point}"

        sequential = str(sequential).zfill(9)

        numeric_code = str(random.randint(10000000, 99999999))

        base_key = (
            f"{date_str}"
            f"{document_type}"
            f"{ruc}"
            f"{environment}"
            f"{serie}"
            f"{sequential}"
            f"{numeric_code}"
            f"{emission_type}"
        )

        dv = SriAccessKeyService.mod11(base_key)

        return base_key + str(dv)
    
    @staticmethod
    def mod11(key):

        weights = [2,3,4,5,6,7]

        total = 0
        weight_index = 0

        for digit in reversed(key):

            total += int(digit) * weights[weight_index]

            weight_index += 1

            if weight_index == len(weights):
                weight_index = 0

        mod = 11 - (total % 11)

        if mod == 11:
            return 0
        if mod == 10:
            return 1

        return mod
    
    """
    Ejemplo de uso
    from sri.services.sri_access_key_service import SriAccessKeyService

    key = SriAccessKeyService.generate_access_key(
        date=document.date,
        document_type="01",
        ruc="0999999999001",
        environment="1",
        establishment="001",
        emission_point="001",
        sequential="123"
    )

    print(key)
    """