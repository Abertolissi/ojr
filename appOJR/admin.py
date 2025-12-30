import decimal
import math
import os
import zipfile
from io import BytesIO
from smtplib import SMTPException

from django.contrib import admin
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

from docx import Document
from docxtpl import DocxTemplate

from .models import (
    AgenciaMaritima, Armadora, ArmadoraPuerto, Barco, Camion, Carga, Chofer,
    Cliente, Combustible, Configuracion, ContactoAgencia, Producto, Puerto,
    Rancho, Remito, RemitoVarios, Remolque, TransferenciaDeposito, Transporte,
    Deposito
)
from .views import admin_cargarCamionesCsv_redirect

# ==============================================================================
# CONFIGURACIÓN GENERAL
# ==============================================================================

admin.site.site_header = 'Aplicacion OJR'

# ==============================================================================
# HELPER FUNCTIONS (Utilitarios y Formateo)
# ==============================================================================

def formato_miles(valor):
    """Formatea un valor numérico a moneda (custom format)."""
    return f"${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==============================================================================
# LÓGICA DE GENERACIÓN DE DOCUMENTOS
# ==============================================================================

def generarRemito(remito):
    configuracion = Configuracion.objects.get(id=1)
    
    # Selección de Template
    if configuracion.impresoraRemitos == 'LaserNuria':
        template_path = os.path.join(os.getcwd(), 'appOJR', 'templates', 'RemitoLaser.docx')
    elif remito.empresa == "OJR":
        template_path = os.path.join(os.getcwd(), 'appOJR', 'templates', 'RemitoOJR.docx')
    else:
        template_path = os.path.join(os.getcwd(), 'appOJR', 'templates', 'RemitoNAO.docx')
        
    doc = DocxTemplate(template_path)

    # Cálculos de VCF
    densidad = remito.carga.densidad * 1000
    if densidad == 0: # Evitar división por cero si densidad no está seteada
        densidad = decimal.Decimal(1)
        
    densidad_sq = densidad ** 2
    
    factor1 = (decimal.Decimal(346.4228) / densidad_sq) + (decimal.Decimal(0.4388) / densidad)
    factor2 = decimal.Decimal(-0.00336312) + (decimal.Decimal(2680.3206) / densidad_sq)
    factor3 = (decimal.Decimal(594.5418) / densidad_sq)
    factor4 = (decimal.Decimal(186.9696) / densidad_sq) + (decimal.Decimal(0.4862) / densidad)

    delta_temp = remito.carga.temperatura - 15
    
    if densidad < decimal.Decimal(770.8):
        exponent = -factor1 * delta_temp * (1 + decimal.Decimal(0.8) * factor1 * delta_temp)
    elif densidad < decimal.Decimal(787.5):
        exponent = -factor2 * delta_temp * (1 + decimal.Decimal(0.8) * factor2 * delta_temp)
    elif densidad < decimal.Decimal(832.3):
        exponent = -factor3 * delta_temp * (1 + decimal.Decimal(0.8) * factor3 * delta_temp)
    else:
        exponent = -factor4 * delta_temp * (1 + decimal.Decimal(0.8) * factor4 * delta_temp)
    
    VCF = round(math.exp(exponent), 5)

    # Textos condicionales
    exentoRancho = "PRODUCTO EXENTO RANCHO" if remito.carga.exentoRancho else ""
    
    nroRancho = ""
    if remito.carga.nroRancho is not None:
        codigo_aduana = str(remito.carga.puerto.codigoAduana).zfill(3)
        nro_rancho_fmt = str(remito.carga.nroRancho).zfill(6)
        letra_rancho = str(remito.carga.letraRancho) if remito.carga.letraRancho else ""
        nroRancho = f"RANCHO {remito.carga.fechaInicio.strftime('%y')} {codigo_aduana} ER02 {nro_rancho_fmt} {letra_rancho}"

    ordenCompra = f"ORDEN DE COMPRA Nº {remito.carga.ordenCompra}" if remito.carga.ordenCompra else ""

    cantidadTotal = math.trunc((decimal.Decimal(remito.cantidadBarco) + decimal.Decimal(remito.cantidadDeposito)) * 1000 * decimal.Decimal(VCF))
    cantidadBarco = math.trunc(decimal.Decimal(remito.cantidadBarco) * 1000 * decimal.Decimal(VCF))
    cantidadDeposito = math.trunc(decimal.Decimal(remito.cantidadDeposito) * 1000 * decimal.Decimal(VCF))

    context = {
        'armadora': remito.carga.barco.armadora.nombre,
        'transporte': remito.transporte.nombre,
        'barco': remito.carga.barco.nombre,
        'puerto': remito.carga.puerto.nombre,
        'cuitArmadora': remito.carga.barco.armadora.cuit,
        'combustible': remito.carga.combustible.nombre,
        'apellidoChofer': remito.chofer.apellido,
        'nombreChofer': remito.chofer.nombre,
        'dniChofer': remito.chofer.dni,
        'marcaCamion': remito.camion.marca,
        'patenteC': remito.camion.patente,
        'marcaR': remito.remolque.marca,
        'patenteR': remito.remolque.patente,
        'cantidadTotal': cantidadTotal,
        'cantidadBarco': cantidadBarco,
        'cantidadDeposito': cantidadDeposito,
        'fc': VCF,
        'azufre': '<<300',
        'den': remito.carga.densidad,
        'temp': remito.carga.temperatura,
        'exentoRancho': exentoRancho,
        'nroRancho': nroRancho,
        'ordenCompra': ordenCompra,
        'dia': remito.carga.fechaRemito.day,
        'mes': remito.carga.fechaRemito.month,
        'ano': remito.carga.fechaRemito.year
    }
    doc.render(context)
    return doc

def generarRemitoVarios(idRemito):
    remito = RemitoVarios.objects.get(id=idRemito)
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = f'attachment; filename="RemitoNro{remito.numero}.docx"'
    
    if remito.empresa == "OJR":
        template_name = 'RemitoVariosOJR.docx'
    else:
        template_name = 'RemitoVariosNAO.docx'
        
    doc = DocxTemplate(os.path.join(os.getcwd(), 'appOJR', 'templates', template_name))
    
    context = {
        'transporte': remito.get_transporte_display(),
        'destinatario': remito.destinatario.denominacion,
        'cuit': remito.destinatario.cuit,
        'lugarEntrega': remito.lugarEntrega,
        'IVA': remito.get_IVA_display(),
        'cantidad': remito.cantidad,
        'unidad': remito.unidad,
        'producto': remito.producto,
        'apellidoChofer': remito.chofer.apellido,
        'nombreChofer': remito.chofer.nombre,
        'dniChofer': remito.chofer.dni,
        'marcaCamion': remito.camion.marca,
        'patenteC': remito.camion.patente,
        'marcaR': remito.remolque.marca,
        'patenteR': remito.remolque.patente,
        'observacion': remito.observacion,
        'dia': remito.fecha.day,
        'mes': remito.fecha.month,
        'ano': remito.fecha.year
    }
    
    doc.render(context)
    doc.save(response)
    return response

def generarDocumentosCamaronesComodoroCaletaCordoba(idCarga, cantidadCombustible, remito, puertoFormulario):
    if puertoFormulario == "Camarones":
        template_name = 'Formularios-Camarones.docx'
    elif puertoFormulario == "Caleta Cordoba":
        template_name = 'Formularios-CaletaCordoba.docx'
    else:
        template_name = 'Formularios-Comodoro.docx'
        
    doc = DocxTemplate(os.path.join(os.getcwd(), 'appOJR', 'templates', template_name))
    
    carga = Carga.objects.get(id=idCarga)
    configuracion = Configuracion.objects.get(id=1)
    
    context = {
        'barco': carga.barco.nombre,
        'agenciaMaritima': carga.barco.armadora.agenciaMaritima.nombre,
        'bandera': carga.barco.bandera,
        'armadora': carga.barco.armadora.nombre,
        'matricula': carga.barco.matricula,
        'apellidoChofer': remito.chofer.apellido,
        'nombreChofer': remito.chofer.nombre,
        'dniChofer': remito.chofer.dni,
        'pnaChofer': remito.chofer.pna,
        'empresa': configuracion.empresa,
        'domicilioEmpresa': configuracion.direccionEmpresa,
        'titularEmpresa': configuracion.titularEmpresa,
        'cuitEmpresa': configuracion.cuitEmpresa,
        'telefonoEmpresa': configuracion.telefonoEmpresa,
        'emailEmpresa': configuracion.emailEmpresa,
        'certificadoInscripcion': configuracion.certificadoInscripcion,
        'vencimientoCertificadoInscripcion': configuracion.vencimientoCertificadoInscripcion.strftime("%d/%m/%Y"),
        'patenteCamion': remito.camion.patente,
        'patenteRemolque': remito.remolque.patente,
        'cantidad': cantidadCombustible * 1000,
        'aseguradoraChoferes': configuracion.aseguradoraChoferes,
        'vencimientoAseguradora': configuracion.vencimientoAseguradora.strftime("%d/%m/%Y"),
        'fechaInicio': carga.fechaInicio.strftime("%d/%m/%Y"),
        'horaInicio': carga.horaInicio.strftime("%H:%M") if carga.horaInicio else ""
    }
    doc.render(context)
    return doc

def generarDocumentosPuertoMadryn(idCarga, cantidadCombustible, cantidadCamiones):
    doc = DocxTemplate(os.path.join(os.getcwd(), 'appOJR', 'templates', 'Formularios-PuertoMadryn.docx'))
    
    carga = Carga.objects.get(id=idCarga)
    configuracion = Configuracion.objects.get(id=1)
    
    # Helper para formatear floats con coma decimal
    def fmt(val):
        return '{0:.3g}'.format(val).replace(",", "@").replace(".", ",").replace("@", ".")

    context = {
        'agenciaMaritima': carga.barco.armadora.agenciaMaritima.nombre,
        'telefonoAgenciaMaritima': carga.barco.armadora.agenciaMaritima.telefono,
        'barco': carga.barco.nombre,
        'matricula': carga.barco.matricula,
        'tipoBuque': carga.barco.tipo,
        'bandera': carga.barco.bandera,
        'eslora': fmt(carga.barco.eslora),
        'manga': fmt(carga.barco.manga),
        'puntal': fmt(carga.barco.puntal),
        'puerto': carga.puerto.nombre,
        'sitioPuerto': carga.sitioPuerto,
        'transportista': configuracion.empresa,
        'telefonoTransportista': configuracion.telefonoEmpresa,
        'tipoCombustible': carga.combustible.nombre,
        'cantidad': cantidadCombustible,
        'cantidadCamiones': cantidadCamiones,
        'vencimientoCertificadoInscripcion': configuracion.vencimientoCertificadoInscripcion.strftime("%d/%m/%Y"),
        'fechaInicio': carga.fechaInicio.strftime("%d/%m/%Y"),
        'horaInicio': carga.horaInicio.strftime("%H:%M") if carga.horaInicio else ""
    }
    doc.render(context)
    return doc

def generarDocumentosRawson(idCarga, cantidadCombustible, cantidadCamiones, remito):
    doc = DocxTemplate(os.path.join(os.getcwd(), 'appOJR', 'templates', 'Formularios-Rawson.docx'))
    
    carga = Carga.objects.get(id=idCarga)
    configuracion = Configuracion.objects.get(id=1)
    
    def fmt(val):
        return '{0:.3g}'.format(val).replace(",", "@").replace(".", ",").replace("@", ".")

    context = {
        'empresa': configuracion.empresa,
        'armadora': carga.barco.armadora.nombre,
        'telefonoArmadora': carga.barco.armadora.telefono,
        'matricula': carga.barco.matricula,
        'apellidoChofer': remito.chofer.apellido,
        'nombreChofer': remito.chofer.nombre,
        'dniChofer': remito.chofer.dni,
        'pnaChofer': remito.chofer.pna,
        'telefonoChofer': remito.chofer.telefono,
        'nacionalidadChofer': remito.chofer.nacionalidad,
        'domicilioChofer': remito.chofer.domicilio,
        'barco': carga.barco.nombre,
        'eslora': fmt(carga.barco.eslora),
        'manga': fmt(carga.barco.manga),
        'puntal': fmt(carga.barco.puntal),
        'marcaCamion': remito.camion.marca,
        'patenteCamion': remito.camion.patente,
        'sitioPuerto': carga.sitioPuerto,
        'titularEmpresa': configuracion.titularEmpresa,
        'cuitEmpresa': configuracion.cuitEmpresa,
        'tipoCombustible': carga.combustible.nombre,
        'cantidad': cantidadCombustible * 1000,
        'cantidadCamiones': cantidadCamiones,
        'fechaInicio': carga.fechaInicio.strftime("%d/%m/%Y"),
        'horaInicio': carga.horaInicio.strftime("%H:%M") if carga.horaInicio else ""
    }
    doc.render(context)
    return doc

def generarDocumentoTransferencia(idTransferencia):
    transferencia = TransferenciaDeposito.objects.get(id=idTransferencia)
    response = HttpResponse(content_type='application/msword')
    filename = f"Transferencia_{transferencia.id}.docx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Usamos RemitoVariosOJR como base
    template_name = 'RemitoVariosOJR.docx' 
    doc = DocxTemplate(os.path.join(os.getcwd(), 'appOJR', 'templates', template_name))
    
    destinatario_nombre = ""
    if transferencia.deposito_destino:
        destinatario_nombre = transferencia.deposito_destino.nombre

    direccion_entrega = ""
    if transferencia.deposito_destino and transferencia.deposito_destino.direccion:
        direccion_entrega = transferencia.deposito_destino.direccion

    transporte_nombre = ""
    if transferencia.camion and transferencia.camion.transporte:
        transporte_nombre = transferencia.camion.transporte.nombre

    # Handle potentially missing relationships safely
    apellido_chofer = transferencia.chofer.apellido if transferencia.chofer else ""
    nombre_chofer = transferencia.chofer.nombre if transferencia.chofer else ""
    dni_chofer = transferencia.chofer.dni if transferencia.chofer else ""
    
    marca_camion = transferencia.camion.marca if transferencia.camion else ""
    patente_camion = transferencia.camion.patente if transferencia.camion else ""

    context = {
        'transporte': transporte_nombre,
        'destinatario': destinatario_nombre,
        'cuit': "", # No hay CUIT especifico de deposito destino interno usualmente
        'lugarEntrega': direccion_entrega,
        'IVA': "Traslado Interno",
        'cantidad': transferencia.cantidad,
        'unidad': "LTS", # Default a Litros para combustibles
        'producto': transferencia.combustible.nombre,
        'apellidoChofer': apellido_chofer,
        'nombreChofer': nombre_chofer,
        'dniChofer': dni_chofer,
        'marcaCamion': marca_camion,
        'patenteC': patente_camion,
        'marcaR': "", # Transferencia no tiene remolque
        'patenteR': "",
        'observacion': transferencia.observaciones or "",
        'dia': transferencia.fecha.day,
        'mes': transferencia.fecha.month,
        'ano': transferencia.fecha.year
    }
    
    doc.render(context)
    doc.save(response)
    return response

def generarDocumentosDeseado(idCarga, cantidadCombustible, cantidadCamiones):
    doc = DocxTemplate(os.path.join(os.getcwd(), 'appOJR', 'templates', 'Formularios-Deseado.docx'))
    
    carga = Carga.objects.get(id=idCarga)
    configuracion = Configuracion.objects.get(id=1)
    
    def fmt(val):
        return '{0:.3g}'.format(val).replace(",", "@").replace(".", ",").replace("@", ".")

    context = {
        'agenciaMaritima': carga.barco.armadora.agenciaMaritima.nombre,
        'telefonoAgenciaMaritima': carga.barco.armadora.agenciaMaritima.telefono,
        'barco': carga.barco.nombre,
        'matricula': carga.barco.matricula,
        'tipoBuque': carga.barco.tipo,
        'bandera': carga.barco.bandera,
        'eslora': fmt(carga.barco.eslora),
        'manga': fmt(carga.barco.manga),
        'puntal': fmt(carga.barco.puntal),
        'puerto': carga.puerto.nombre,
        'sitioPuerto': carga.sitioPuerto,
        'transportista': configuracion.empresa,
        'telefonoTransportista': configuracion.telefonoEmpresa,
        'tipoCombustible': carga.combustible.nombre,
        'cantidad': cantidadCombustible,
        'cantidadCamiones': cantidadCamiones,
        'vencimientoCertificadoInscripcion': configuracion.vencimientoCertificadoInscripcion.strftime("%d/%m/%Y"),
        'fechaInicio': carga.fechaInicio.strftime("%d/%m/%Y"),
        'horaI': carga.horaInicio.strftime("%H:%M") if carga.horaInicio else "",
        'horaF': carga.horaInicio.strftime("%H:%M") if carga.horaInicio else ""
    }
    doc.render(context)
    return doc

def generarDocumentos(idCarga):
    documentos = []
    carga = Carga.objects.get(id=idCarga)
    remitos_de_carga = carga.remito_set.all()

    i = 0
    cantidadCombustible = 0
    for remito in remitos_de_carga:
        i += 1
        doc = generarRemito(remito)
        doc_io = BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        documentos.append(('Remito{}.docx'.format(i), doc_io))
        cantidadCombustible += remito.cantidadBarco # Asumiendo acumulación

    # Generar el documento de Carga
    if not remitos_de_carga.exists():
        # Manejo simple si no hay remitos, aunque debería haber lógica de negocio aquí.
        # Retornamos vacío o error manejado, pero por ahora mantengo estructura
        pass 
    else:
        primer_remito = remitos_de_carga[0]
        
        if carga.puerto.nombre in ['Camarones', 'Comodoro Rivadavia', 'Caleta Cordoba']:
            doc = generarDocumentosCamaronesComodoroCaletaCordoba(idCarga, cantidadCombustible, primer_remito, carga.puerto.nombre)
        elif carga.puerto.nombre in ['Almirante Storni', 'Almirante Luis Piedra Buena']:
            doc = generarDocumentosPuertoMadryn(idCarga, cantidadCombustible, i)
        elif carga.puerto.nombre in ['Puerto Deseado']:
            doc = generarDocumentosDeseado(idCarga, cantidadCombustible, i)
        else:
            doc = generarDocumentosRawson(idCarga, cantidadCombustible, i, primer_remito)

        doc_io = BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        documentos.append(('Carga.docx', doc_io))

    return documentos

def generarDocumentosZip(idCarga):
    documentos = generarDocumentos(idCarga)
    zip_io = BytesIO()
    
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for filename, doc_io in documentos:
            zip_file.writestr(filename, doc_io.getvalue())

    carga = Carga.objects.get(id=idCarga)
    response = HttpResponse(content_type='application/zip')
    
    # Construcción filename
    fecha_str = f"{carga.fechaInicio.day}{carga.fechaInicio.month}{carga.fechaInicio.year}"
    filename = f"{carga.barco}{fecha_str}.zip"
    
    response['Content-Disposition'] = f'attachment; filename={filename}'
    response.write(zip_io.getvalue())
    return response

# ==============================================================================
# ACTIONS (Acciones de Admin)
# ==============================================================================

@admin.action(description="Enviar solicitud de Rancho por correo")
def enviar_solicitud_rancho(modeladmin, request, queryset):
    for rancho in queryset:
        if rancho.emailEnviado:
            continue
        
        barco = rancho.barco
        armadora = barco.armadora
        agencia = armadora.agenciaMaritima

        contactos = ContactoAgencia.objects.filter(agenciaMaritima=agencia, enviaRancho=True)

        if not contactos.exists():
            continue

        precio_sin_iva = rancho.precio or Decimal(0)
        impuestos = rancho.impuestos or Decimal(0)
        precio_con_iva = precio_sin_iva * decimal.Decimal("1.21")
        litros = rancho.litros or 0

        total_sin_iva = (precio_sin_iva + impuestos) * litros
        total_con_iva = (precio_con_iva + impuestos) * litros

        subject = f"Solicitud de Rancho Barco {barco.nombre}"
        message = f"""
        Solicitud de Rancho

        Fecha: {timezone.now().strftime('%d/%m/%Y')}
        Barco: {barco.nombre}
        Armadora: {armadora.nombre}
        Puerto de Carga: {rancho.puerto}
        Fecha de carga: {rancho.fechaCarga.strftime('%d/%m/%Y')}
        Producto: {rancho.combustible.nombre}
        Litros: {litros}
        Marca: {rancho.empresa}
        Origen Mercaderia: Neuquén
        Densidad: {rancho.densidad}
        Azufre: {formato_miles(rancho.azufre)}
        Precio sin IVA: {formato_miles(precio_sin_iva)}
        Impuestos: {formato_miles(impuestos)}
        Precio con IVA: {formato_miles(precio_con_iva)}
        Precio Total sin IVA: {formato_miles(total_sin_iva)}
        Precio Total con IVA: {formato_miles(total_con_iva)}
        """
        envio_exitoso = False

        for contacto in contactos:
            try:
                send_mail(
                    subject,
                    message,
                    'transporteOJR@gmail.com.ar',
                    [contacto.correoElectronico],
                    fail_silently=False,
                )
                envio_exitoso = True
            except (BadHeaderError, SMTPException) as e:
                print(f"[ERROR] No se pudo enviar correo a {contacto.correoElectronico} - Error: {e}")
                continue

        if envio_exitoso:
            rancho.emailEnviado = True
            rancho.save()

def imprimirFormulario(modeladmin, request, queryset):
    for obj in queryset:
        return generarDocumentosZip(obj.id)
imprimirFormulario.short_description = "Imprime Formulario"

def imprimirRemitoVariosAction(modeladmin, request, queryset):
    for obj in queryset:
        return generarRemitoVarios(obj.id)
imprimirRemitoVariosAction.short_description = "Imprime Remitos Varios"

def imprimirFormularioTransferencia(modeladmin, request, queryset):
    for obj in queryset:
        return generarDocumentoTransferencia(obj.id)
imprimirFormularioTransferencia.short_description = "Imprime Formulario Transferencia"

# ==============================================================================
# INLINES
# ==============================================================================

class detalle_CargaInline(admin.TabularInline):
    model = Remito
    extra = 1

# ==============================================================================
# MODEL ADMINS
# ==============================================================================

class ArmadoraPuertoAdmin(admin.ModelAdmin):
    list_display = ('id', 'armadora', 'puerto', 'agenciaMaritima')
    search_fields = ('id', 'destinatario') # Nota: 'destinatario' no parece ser campo de ArmadoraPuerto, revisar modelo

class BarcoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'matricula', 'armadora')
    search_fields = ('id', 'nombre', 'armadora__nombre')

class CamionAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'patente', 'transporte', 'habilitadoAFIP')
    search_fields = ('id', 'patente')

class CargaAdmin(admin.ModelAdmin):
    class Media:
        js = ("js/dynamic_camiones_select.js", "js/dynamic_remolques_select.js",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('getCamiones/', self.getCamiones),
        ]
        return my_urls + urls

    def getCamiones(self, request):
        transporte_id = request.GET.get('transporte_id')
        camiones = Camion.objects.filter(transporte_id=transporte_id).values_list('id', 'patente')
        return JsonResponse({'camiones': dict(camiones)})
    
    inlines = (detalle_CargaInline,)
    list_display = ('id', 'barco', 'fechaInicio')
    search_fields = ('id', 'barco__nombre')
    actions = [imprimirFormulario]

class ContactoAgenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'agenciaMaritima', 'correoElectronico', 'enviaRancho')
    search_fields = ('id', 'agenciaMaritima__nombre', 'correoElectronico')

class DepositoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion')
    search_fields = ('id', 'nombre')

class RanchoAdmin(admin.ModelAdmin):
    list_display = ('id', 'barco', 'puerto', 'fechaCarga', 'litros', 'emailEnviado')
    search_fields = ('id', 'barco__nombre')
    actions = [enviar_solicitud_rancho]

class RemitoVariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'destinatario', 'fecha')
    search_fields = ('id', 'destinatario__denominacion')
    actions = [imprimirRemitoVariosAction]

class RemolqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'patente')
    search_fields = ('id', 'patente')


class TransferenciaDepositoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'fecha', 'combustible', 'deposito_origen', 'deposito_destino',
        'cantidad', 'chofer', 'camion'
    )
    search_fields = ('id', 'deposito_origen__nombre', 'deposito_destino__nombre')

    list_filter = ('combustible',)
    actions = [imprimirFormularioTransferencia]

# ==============================================================================
# CUSTOM ADMIN SITE
# ==============================================================================

class MyAdminSite(admin.AdminSite):
    site_header = 'Aplicacion OJR'
    index_template = 'admin/custom_index.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('cargarCamionesCsv/', self.admin_view(admin_cargarCamionesCsv_redirect), name='admin_cargarCamionesCsv')
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_menu_links'] = [
            {
                'url': reverse('cargarCamionesCsv'),
                'name': 'CargarCamionesAFIP',
            }
        ]
        return super().index(request, extra_context)

admin_site = MyAdminSite(name='myadmin')

# ==============================================================================
# REGISTRO DE MODELOS
# ==============================================================================

# Registro en Admin Default
admin.site.register(AgenciaMaritima)
admin.site.register(Armadora)
admin.site.register(ArmadoraPuerto, ArmadoraPuertoAdmin)
admin.site.register(Barco, BarcoAdmin)
admin.site.register(Camion, CamionAdmin)
admin.site.register(Carga, CargaAdmin)
admin.site.register(Chofer)
admin.site.register(Cliente)
admin.site.register(Combustible)
admin.site.register(Configuracion)
admin.site.register(ContactoAgencia, ContactoAgenciaAdmin)
admin.site.register(Producto)
admin.site.register(Puerto)
admin.site.register(Rancho, RanchoAdmin)
admin.site.register(RemitoVarios, RemitoVariosAdmin)
admin.site.register(Remolque, RemolqueAdmin)
admin.site.register(Deposito, DepositoAdmin)
admin.site.register(TransferenciaDeposito, TransferenciaDepositoAdmin)
admin.site.register(Transporte)

# Registro en Admin Custom (MyAdminSite)
# Nota: Se registran todos para mantener paridad, aunque si solo se usa uno 
# en producción, se podría eliminar el otro set.
model_admin_pairs = [
    (AgenciaMaritima, None),
    (Armadora, None),
    (ArmadoraPuerto, ArmadoraPuertoAdmin),
    (Barco, BarcoAdmin),
    (Camion, CamionAdmin),
    (Carga, CargaAdmin),
    (Chofer, None),
    (Cliente, None),
    (Combustible, None),
    (Configuracion, None),
    (ContactoAgencia, ContactoAgenciaAdmin),
    (Producto, None),
    (Puerto, None),
    (Rancho, RanchoAdmin),
    (RemitoVarios, RemitoVariosAdmin),
    (Remolque, RemolqueAdmin),
    (TransferenciaDeposito, TransferenciaDepositoAdmin),
    (Transporte, None),
    (Deposito, DepositoAdmin),
]

for model, admin_class in model_admin_pairs:
    admin_site.register(model, admin_class)
