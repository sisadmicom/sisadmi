import xml.etree.ElementTree as ET


class SriXMLService:

    @staticmethod
    def generate_invoice_xml(document):

        factura = ET.Element("factura")

        factura.append(
            SriXMLService.info_tributaria(document)
        )

        factura.append(
            SriXMLService.info_factura(document)
        )

        factura.append(
            SriXMLService.detalles(document)
        )

        return ET.tostring(
            factura,
            encoding="utf-8",
            method="xml"
        )
    
    @staticmethod
    def info_tributaria(document):

        info = ET.Element("infoTributaria")

        ET.SubElement(info, "ambiente").text = "1"

        ET.SubElement(info, "tipoEmision").text = "1"

        ET.SubElement(info, "razonSocial").text = "MI EMPRESA"

        ET.SubElement(info, "ruc").text = "0999999999001"

        ET.SubElement(info, "claveAcceso").text = document.access_key

        ET.SubElement(info, "codDoc").text = "01"

        ET.SubElement(info, "estab").text = "001"

        ET.SubElement(info, "ptoEmi").text = "001"

        ET.SubElement(info, "secuencial").text = document.sri_number[-9:]

        ET.SubElement(info, "dirMatriz").text = "GUAYAQUIL"

        return info
    
    @staticmethod
    def info_factura(document):

        info = ET.Element("infoFactura")

        ET.SubElement(info, "fechaEmision").text = document.date.strftime("%d/%m/%Y")

        ET.SubElement(info, "dirEstablecimiento").text = "GUAYAQUIL"

        ET.SubElement(info, "tipoIdentificacionComprador").text = "05"

        ET.SubElement(info, "razonSocialComprador").text = document.partner.name

        ET.SubElement(info, "identificacionComprador").text = document.partner.vat

        ET.SubElement(info, "totalSinImpuestos").text = str(document.subtotal)

        ET.SubElement(info, "importeTotal").text = str(document.total)

        return info
    
    @staticmethod
    def detalles(document):

        detalles = ET.Element("detalles")

        for line in document.lines.all():

            detalle = ET.SubElement(detalles, "detalle")

            ET.SubElement(detalle, "codigoPrincipal").text = line.product.code

            ET.SubElement(detalle, "descripcion").text = line.product.name

            ET.SubElement(detalle, "cantidad").text = str(line.qty)

            ET.SubElement(detalle, "precioUnitario").text = str(line.price)

            ET.SubElement(detalle, "precioTotalSinImpuesto").text = str(line.subtotal)

        return detalles
"""
Uso
    @staticmethod
    def detalles(document):

        detalles = ET.Element("detalles")

        for line in document.lines.all():

            detalle = ET.SubElement(detalles, "detalle")

            ET.SubElement(detalle, "codigoPrincipal").text = line.product.code

            ET.SubElement(detalle, "descripcion").text = line.product.name

            ET.SubElement(detalle, "cantidad").text = str(line.qty)

            ET.SubElement(detalle, "precioUnitario").text = str(line.price)

            ET.SubElement(detalle, "precioTotalSinImpuesto").text = str(line.subtotal)

        return detalles

        xml = models.TextField(
    blank=True,
    null=True
)
xml = models.TextField(
    blank=True,
    null=True
)
"""