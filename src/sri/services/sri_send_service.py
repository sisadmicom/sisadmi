import base64
from zeep import Client


class SriSendService:

    RECEPCION_URL = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl"

    AUTORIZACION_URL = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl"

    @staticmethod
    def send_xml(xml_signed):

        client = Client(SriSendService.RECEPCION_URL)

        xml_base64 = base64.b64encode(xml_signed).decode()

        response = client.service.validarComprobante(xml_base64)

        return response
    
    @staticmethod
    def authorize(access_key):

        client = Client(SriSendService.AUTORIZACION_URL)

        response = client.service.autorizacionComprobante(access_key)

        return response
    
"""
Uso del servicio 
    Enviar XML
    from sri.services.sri_send_service import SriSendService

response = SriSendService.send_xml(
    document.xml_signed.encode()
)
    COnsultar XML
    auth = SriSendService.authorize(
    document.access_key
)
"""