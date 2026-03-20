from signxml import XMLSigner
from lxml import etree
from cryptography.hazmat.primitives.serialization import pkcs12


class SriSignatureService:

    @staticmethod
    def sign_xml(xml_string, p12_file, password):

        # cargar certificado
        with open(p12_file, "rb") as f:
            p12_data = f.read()

        private_key, certificate, additional = pkcs12.load_key_and_certificates(
            p12_data,
            password.encode()
        )

        xml = etree.fromstring(xml_string)

        signer = XMLSigner()

        signed_root = signer.sign(
            xml,
            key=private_key,
            cert=certificate
        )

        return etree.tostring(
            signed_root,
            pretty_print=True,
            encoding="utf-8"
        )
    
"""
Uso del servicio

from signxml import XMLSigner
from lxml import etree
from cryptography.hazmat.primitives.serialization import pkcs12


class SriSignatureService:

    @staticmethod
    def sign_xml(xml_string, p12_file, password):

        # cargar certificado
        with open(p12_file, "rb") as f:
            p12_data = f.read()

        private_key, certificate, additional = pkcs12.load_key_and_certificates(
            p12_data,
            password.encode()
        )

        xml = etree.fromstring(xml_string)

        signer = XMLSigner()

        signed_root = signer.sign(
            xml,
            key=private_key,
            cert=certificate
        )

        return etree.tostring(
            signed_root,
            pretty_print=True,
            encoding="utf-8"
        )
"""