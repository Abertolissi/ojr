import os
from django.contrib import admin
from django.http import HttpResponse
from docxtpl import DocxTemplate
from docx import Document
from docx.shared import Inches
import decimal
import math
import os
import zipfile
from io import BytesIO
from django.http import HttpResponse,JsonResponse
from django.urls import path, reverse
from .views import admin_cargarCamionesCsv_redirect
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.core.mail import send_mail
from django.utils.html import format_html
from .models import Rancho, ContactoAgencia
from decimal import Decimal
from .models import Armadora, ArmadoraPuerto, Barco, Carga, Chofer, Cliente, ContactoAgencia, Producto, Puerto, Combustible, Camion, AgenciaMaritima, Configuracion, Remito, RemitoVarios, Remolque, Transporte, Rancho


# Register your models here.

admin.site.register(AgenciaMaritima)
admin.site.register(Armadora)   
admin.site.register(Barco)
admin.site.register(Chofer)
admin.site.register(Cliente)
admin.site.register(Combustible)
admin.site.register(Configuracion)
admin.site.register(ContactoAgencia)
admin.site.register(Puerto)
admin.site.register(Transporte)
admin.site.register(Producto)



admin.site.site_header = 'Aplicacion OJR'

@admin.action(description="Enviar solicitud de Rancho por correo")
def enviar_solicitud_rancho(modeladmin, request, queryset):
    for rancho in queryset:
        barco = rancho.barco
        armadora = barco.armadora
        agencia = armadora.agenciaMaritima

        # Obtener contactos
        contactos = ContactoAgencia.objects.filter(agenciaMaritima=agencia, enviaRancho=True)

        if not contactos.exists():
            continue  # No hay contactos, pasar al siguiente rancho

        # Cálculos
        precio_sin_iva = rancho.precio or Decimal(0)
        impuestos = rancho.impuestos or Decimal(0)
        precio_con_iva = precio_sin_iva * Decimal("1.21")  # Supone 21% de IVA
        litros = rancho.litros or 0

        total_sin_iva = (precio_sin_iva + impuestos) * litros
        total_con_iva = (precio_con_iva + impuestos) * litros

        subject = "Solicitud de Rancho Barco"
        message = f"""
        Solicitud de Rancho

        Fecha: {rancho.fechaCarga.strftime('%d/%m/%Y')}
        Barco: {barco.nombre}
        Armadora: {armadora.nombre}
        Fecha de carga: {rancho.fechaCarga.strftime('%d/%m/%Y')}
        Litros: {litros}
        Producto: {rancho.combustible.nombre}
        Marca: (Completar si tenés el dato en otro campo)
        Origen: Neuquén
        Densidad: {rancho.densidad}
        Azufre: {rancho.azufre}
        Precio sin IVA: ${precio_sin_iva}
        Impuestos: ${impuestos}
        Precio con IVA: ${precio_con_iva}
        Precio Total sin IVA: ${total_sin_iva}
        Precio Total con IVA: ${total_con_iva}
        """

        for contacto in contactos:
            send_mail(
                subject,
                message,
                'tu-correo@tudominio.com',  # Remitente
                [contacto.correoElectronico],
                fail_silently=False,
            )

def imprimirFormulario(modeladmin, request, queryset):

    for obj in queryset:
        # Acceder al ID del objeto seleccionado
        response=generarDocumentosZip(obj.id)
        return response
    
    imprimirFormulario.short_description = "Imprime Formulario"

def imprimirRemitoVarios(modeladmin, request, queryset):

    for obj in queryset:
        # Acceder al ID del objeto seleccionado
        response=generarRemitoVarios(obj.id)
        return response
    
    imprimirFormulario.short_description = "Imprime Remitos Varios"
    
class detalle_CargaInline(admin.TabularInline):
    model = Remito
    extra = 1
    
class CargaAdmin(admin.ModelAdmin):
    #nuevo
    class Media:
        
        js = ("js/dynamic_camiones_select.js",
              "js/dynamic_remolques_select.js",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('getCamiones/', self.getCamiones),
        ]
        return my_urls + urls

    def getCamiones(self, request):
        transporte_id = request.GET.get('transporte_id')
        camiones = Camion.objects.filter(transporte_id=transporte_id).values_list('id', 'patente')
        camiones_dict = dict(camiones)
        return JsonResponse({'camiones': camiones_dict})
    
    #nuevo
    inlines = (detalle_CargaInline,)
    list_display = ('id', 'barco', 'fechaHoraInicio')
    search_fields = ('id', 'barco.nombre')
    actions = [imprimirFormulario]  # Add custom actions to perform bulk operations

admin.site.register(Carga, CargaAdmin)

class CamionAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'patente', 'transporte', 'habilitadoAFIP')
    search_fields = ('id', 'patente')

admin.site.register(Camion, CamionAdmin)   

class RanchoAdmin(admin.ModelAdmin):
    readonly_fields = ('emailEnviado',) 
    list_display = ('id','barco', 'puerto',	'fechaCarga', 'litros', 'emailEnviado')
    search_fields = ('id', 'barco')
    actions = [enviar_solicitud_rancho]  # Add custom actions to perform bulk operations
    
admin.site.register(Rancho, RanchoAdmin)   

class RemolqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'patente')
    search_fields = ('id', 'patente')

admin.site.register(Remolque, RemolqueAdmin) 

class RemitoVariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'destinatario', 'fecha')
    search_fields = ('id', 'destinatario')
    actions = [imprimirRemitoVarios]  # Add custom actions to perform bulk operations

admin.site.register(RemitoVarios,RemitoVariosAdmin)

class ArmadoraPuertoAdmin(admin.ModelAdmin):
    list_display = ('id', 'armadora', 'puerto', 'agenciaMaritima' )
    search_fields = ('id', 'destinatario')


admin.site.register(ArmadoraPuerto, ArmadoraPuertoAdmin )


def generarDocumentosZip(idCarga):
    # Generar documentos
    documentos = generarDocumentos(idCarga)

    # Crear un archivo ZIP en memoria
    zip_io = BytesIO()
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for filename, doc_io in documentos:
            zip_file.writestr(filename, doc_io.getvalue())

    # Crear la respuesta HTTP con el archivo ZIP
    carga = Carga.objects.get(id=idCarga )
    response = HttpResponse(content_type='application/zip')
    filename = str(carga.barco)+ str(carga.fechaHoraInicio.day)+str(carga.fechaHoraInicio.month)+str(carga.fechaHoraInicio.year) + '.zip'
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response.write(zip_io.getvalue())

    return response

def generarDocumentos(idCarga):

    documentos = []

    carga = Carga.objects.get(id=idCarga )

    # Generar todos los remitos de la carga
    remitos_de_carga = carga.remito_set.all()  # Utiliza el nombre del modelo en minúsculas seguido de _set.all()

    # Iterar sobre los remitos
    i=0
    cantidadCombustible=0
    for remito in remitos_de_carga:
        i=i+1
        doc = generarRemito(remito)
        doc_io = BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        documentos.append(('Remito{}.docx'.format(i), doc_io))
        cantidadCombustible = cantidadCombustible + remito.cantidadBarco

        
      # Generar el documento de Carga. i = cantidadCamiones
    if carga.puerto.nombre in  ['Camarones', 'Comodoro Rivadavia', 'Caleta Cordoba' ]:
        doc=generarDocumentosCamaronesComodoroCaletaCordoba(idCarga, cantidadCombustible,remitos_de_carga[0],carga.puerto.nombre);
    elif carga.puerto.nombre in ['Puerto Madryn', 'PIEDRABUENA']:
        doc= generarDocumentosPuertoMadryn(idCarga,cantidadCombustible,i);
    elif carga.puerto.nombre in ['Puerto Deseado']:

        doc= generarDocumentosDeseado(idCarga,cantidadCombustible,i);
    else:
        doc=generarDocumentosRawson(idCarga,cantidadCombustible,i,remitos_de_carga[0]);

   
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
        
    documentos.append(('Carga.docx', doc_io))



    return documentos

def generarRemito(remito):

    configuracion  = Configuracion.objects.get(id=1)
    if configuracion.impresoraRemitos== 'LaserNuria':
        doc = DocxTemplate(os.getcwd() + '/appOJR/templates/RemitoLaser.docx')
    else:
        if (remito.empresa ==  "OJR"):
            doc = DocxTemplate(os.getcwd() + '/appOJR/templates/RemitoOJR.docx')
        else:    
            doc = DocxTemplate(os.getcwd() + '/appOJR/templates/RemitoNAO.docx') 
            
    densidad = remito.carga.densidad*1000
    factor1 =(decimal.Decimal(346.4228)/(densidad**2))+(decimal.Decimal(0.4388)/densidad)
    factor2 =decimal.Decimal(-0.00336312) +(decimal.Decimal(2680.3206)/densidad**2)
    factor3 = (decimal.Decimal(594.5418)/(densidad**2))
    factor4= (decimal.Decimal(186.9696)/(densidad**2))+(decimal.Decimal(0.4862)/densidad)
    if (densidad <decimal.Decimal(770.8)):
        VCF = round(math.exp(-factor1*(remito.carga.temperatura-15)*(1+decimal.Decimal(0.8)*factor1*(remito.carga.temperatura-15))),5)
    elif (densidad <decimal.Decimal(787.5)):      
        VCF = round(math.exp(-factor2*(remito.carga.temperatura-15)*(1+decimal.Decimal(0.8)*factor2*(remito.carga.temperatura-15))),5)
    elif (densidad <decimal.Decimal(832.3)):      
        VCF = round(math.exp(-factor3*(remito.carga.temperatura-15)*(1+decimal.Decimal(0.8)*factor3*(remito.carga.temperatura-15))),5)
    else:
        VCF = round(math.exp(-factor4*(remito.carga.temperatura-15)*(1+decimal.Decimal(0.8)*factor4*(remito.carga.temperatura-15))),5)   

    exentoRancho = ""
    nroRancho = ""
    ordenCompra=""
    transporte=""
    if (remito.carga.exentoRancho == True):
        exentoRancho = "PRODUCTO EXENTO RANCHO"

    if (remito.carga.nroRancho is not None  ):
        nroRancho = "RANCHO " + remito.carga.fechaHoraInicio.strftime("%y") + " " +  str(remito.carga.puerto.codigoAduana).zfill(3) 
        nroRancho = nroRancho + " ER02 " + str(remito.carga.nroRancho).zfill(6) + " " + str(remito.carga.letraRancho)

    if (remito.carga.ordenCompra  is not None ):
        ordenCompra = "ORDEN DE COMPRA Nº " + remito.carga.ordenCompra

    context =  {
                'armadora' : remito.carga.barco.armadora.nombre,
                'transporte' : remito.transporte.nombre, 
                'barco' : remito.carga.barco.nombre,
                'puerto' : remito.carga.puerto.nombre,
                'cuitArmadora' : remito.carga.barco.armadora.cuit,
                'combustible' : remito.carga.combustible.nombre,
                'apellidoChofer' : remito.chofer.apellido,
                'nombreChofer' : remito.chofer.nombre,
                'dniChofer' : remito.chofer.dni,
                'marcaCamion' : remito.camion.marca,
                'patenteC' : remito.camion.patente,
                'marcaR' : remito.remolque.marca,
                'patenteR' : remito.remolque.patente,
                'cantidadTotal' :math.trunc((decimal.Decimal(remito.cantidadBarco) + decimal.Decimal(remito.cantidadDeposito)) * decimal.Decimal(1000) * decimal.Decimal(VCF)),
                'cantidadBarco' :math.trunc((decimal.Decimal(remito.cantidadBarco) * decimal.Decimal(1000) * decimal.Decimal(VCF))),
                'cantidadDeposito' :math.trunc(decimal.Decimal(remito.cantidadDeposito) * decimal.Decimal(1000) * decimal.Decimal(VCF)),
                'fc' : VCF,
                'azufre' : '<<300',
                'den' :remito.carga.densidad ,
                'temp' :remito.carga.temperatura ,
                'exentoRancho': exentoRancho, 
                'nroRancho' : nroRancho,
                'ordenCompra' : ordenCompra,
                'marcaR' : remito.remolque.marca,
                'patenteR' : remito.remolque.patente,
                'dia' : remito.carga.fechaHoraInicio.day,
                'mes' : remito.carga.fechaHoraInicio.month,
                'ano' : remito.carga.fechaHoraInicio.year
                }
    doc.render(context)
    return doc

def generarDocumentosCamaronesComodoroCaletaCordoba(idCarga,cantidadCombustible,remito, puertoFormulario):

    doc = Document()
    if (puertoFormulario =="Camarones"):
        doc = DocxTemplate(os.getcwd() + '/appOJR/templates/Formularios-Camarones.docx')
    elif (puertoFormulario =="Caleta Cordoba"):
        doc = DocxTemplate(os.getcwd() + '/appOJR/templates/Formularios-CaletaCordoba.docx')
    else:
        doc = DocxTemplate(os.getcwd() + '/appOJR/templates/Formularios-Comodoro.docx')
    carga = Carga.objects.get(id=idCarga)
    configuracion  = Configuracion.objects.get(id=1)
    context =  {'barco' : carga.barco.nombre,
                'bandera' : carga.barco.bandera,
                'armadora' : carga.barco.armadora.nombre,
                'matricula' : carga.barco.matricula,
                'apellidoChofer' : remito.chofer.apellido,
                'nombreChofer' : remito.chofer.nombre,
                'dniChofer' : remito.chofer.dni,
                'pnaChofer' :remito.chofer.pna,
                'empresa' : configuracion.empresa,
                'domicilioEmpresa' : configuracion.direccionEmpresa,
                'titularEmpresa' : configuracion.titularEmpresa,
                'cuitEmpresa' : configuracion.cuitEmpresa,
                'telefonoEmpresa' : configuracion.telefonoEmpresa,
                'emailEmpresa' : configuracion.emailEmpresa,
                'certificadoInscripcion' : configuracion.certificadoInscripcion,
                'vencimientoCertificadoInscripcion' : configuracion.vencimientoCertificadoInscripcion.strftime("%d/%m/%Y"),
                'patenteCamion' :remito.camion.patente,
                'patenteRemolque' :remito.remolque.patente,
                 'cantidad' :cantidadCombustible * 1000,
                'aseguradoraChoferes' :configuracion.aseguradoraChoferes,
                'vencimientoAseguradora' :configuracion.vencimientoAseguradora.strftime("%d/%m/%Y"),
                'fechaInicio' : carga.fechaHoraInicio.strftime("%d/%m/%Y"),
                'horaInicio' : carga.fechaHoraInicio.strftime("%H:%M")}
    doc.render(context)
    return doc
    

def generarDocumentosPuertoMadryn(idCarga,cantidadCombustible,cantidadCamiones):
  
    doc = DocxTemplate(os.getcwd() + '/appOJR/templates/Formularios-PuertoMadryn.docx')
  
    carga = Carga.objects.get(id=idCarga )
    configuracion  = Configuracion.objects.get(id=1)
    context =  {'agenciaMaritima' : carga.barco.armadora.agenciaMaritima.nombre, 
                'telefonoAgenciaMaritima' : carga.barco.armadora.agenciaMaritima.telefono,
                'barco' : carga.barco.nombre,
                'matricula' : carga.barco.matricula,
                'tipoBuque': carga.barco.tipo,
                'bandera' : carga.barco.bandera,
                'eslora' : '{0:.3g}'.format(carga.barco.eslora).replace(",", "@").replace(".", ",").replace("@", "."),
                'manga' : '{0:.3g}'.format(carga.barco.manga).replace(",", "@").replace(".", ",").replace("@", "."),
                'puntal' :  '{0:.3g}'.format(carga.barco.puntal).replace(",", "@").replace(".", ",").replace("@", "."),
                'puerto' : carga.puerto.nombre,
                'sitioPuerto' :carga.sitioPuerto,
                'transportista' : configuracion.empresa,
                'telefonoTransportista' :configuracion.telefonoEmpresa,
                'tipoCombustible' : carga.combustible.nombre,
                'cantidad' :cantidadCombustible,
                'cantidadCamiones' : cantidadCamiones,
                'vencimientoCertificadoInscripcion' : configuracion.vencimientoCertificadoInscripcion.strftime("%d/%m/%Y"),
                'fechaInicio' : carga.fechaHoraInicio.strftime("%d/%m/%Y  %H:%M")
    }
    doc.render(context)
    return doc

def generarDocumentosRawson(idCarga,cantidadCombustible,cantidadCamiones, remito):
    
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename="Formularios-Rawson.docx"'

    doc = DocxTemplate(os.getcwd() + '/appOJR/templates/Formularios-Rawson.docx')
  
    carga = Carga.objects.get(id=idCarga )
    configuracion  = Configuracion.objects.get(id=1)
    context =  {'empresa' : configuracion.empresa, 
                'armadora' : carga.barco.armadora.nombre, 
                'telefonoArmadora' : carga.barco.armadora.telefono, 
                'matricula' : carga.barco.matricula,
                'apellidoChofer' : remito.chofer.apellido,
                'nombreChofer' : remito.chofer.nombre,
                'dniChofer' : remito.chofer.dni,
                'pnaChofer' :remito.chofer.pna,
                'telefonoChofer' :remito.chofer.telefono,
                'nacionalidadChofer' :remito.chofer.nacionalidad,
                'domicilioChofer' :remito.chofer.domicilio,
                'barco' : carga.barco.nombre,
                'eslora' : '{0:.3g}'.format(carga.barco.eslora).replace(",", "@").replace(".", ",").replace("@", "."),
                'manga' : '{0:.3g}'.format(carga.barco.manga).replace(",", "@").replace(".", ",").replace("@", "."),
                'puntal' :  '{0:.3g}'.format(carga.barco.puntal).replace(",", "@").replace(".", ",").replace("@", "."),
                'marcaCamion' : remito.camion.marca,
                'patenteCamion' : remito.camion.patente,
                'sitioPuerto' :carga.sitioPuerto,
                'empresa' : configuracion.empresa,
                'titularEmpresa' : configuracion.titularEmpresa,
                'cuitEmpresa' : configuracion.cuitEmpresa,
                'tipoCombustible' : carga.combustible.nombre,
                'cantidad' :cantidadCombustible*1000,
                'cantidadCamiones' : cantidadCamiones,
                'fechaInicio' : carga.fechaHoraInicio.strftime("%d/%m/%Y"),
                'horaInicio' : carga.fechaHoraInicio.strftime("%H:%M")}
    doc.render(context)
    return doc

def generarDocumentosDeseado(idCarga,cantidadCombustible,cantidadCamiones):
  
    doc = DocxTemplate(os.getcwd() + '/appOJR/templates/Formularios-Deseado.docx')
  
    carga = Carga.objects.get(id=idCarga )
    configuracion  = Configuracion.objects.get(id=1)
    context =  {'agenciaMaritima' : carga.barco.armadora.agenciaMaritima.nombre, 
                'telefonoAgenciaMaritima' : carga.barco.armadora.agenciaMaritima.telefono,
                'barco' : carga.barco.nombre,
                'matricula' : carga.barco.matricula,
                'tipoBuque': carga.barco.tipo,
                'bandera' : carga.barco.bandera,
                'eslora' : '{0:.3g}'.format(carga.barco.eslora).replace(",", "@").replace(".", ",").replace("@", "."),
                'manga' : '{0:.3g}'.format(carga.barco.manga).replace(",", "@").replace(".", ",").replace("@", "."),
                'puntal' :  '{0:.3g}'.format(carga.barco.puntal).replace(",", "@").replace(".", ",").replace("@", "."),
                'puerto' : carga.puerto.nombre,
                'sitioPuerto' :carga.sitioPuerto,
                'transportista' : configuracion.empresa,
                'telefonoTransportista' :configuracion.telefonoEmpresa,
                'tipoCombustible' : carga.combustible.nombre,
                'cantidad' :cantidadCombustible,
                'cantidadCamiones' : cantidadCamiones,
                'vencimientoCertificadoInscripcion' : configuracion.vencimientoCertificadoInscripcion.strftime("%d/%m/%Y"),
                'fechaInicio' : carga.fechaHoraInicio.strftime("%d/%m/%Y  %H:%M")
    }
    doc.render(context)
    return doc


def generarRemitoVarios(idRemito):
       
    remito = RemitoVarios.objects.get(id=idRemito )
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename="RemitoNro"' + str(remito.numero) + '".docx"'
    if (remito.empresa ==  "OJR"):
        doc = DocxTemplate(os.getcwd() + '/appOJR/templates/RemitoVariosOJR.docx')
    else:    
        doc = DocxTemplate(os.getcwd() + '/appOJR/templates/RemitoVariosNAO.docx') 
    
    configuracion  = Configuracion.objects.get(id=1)
    context =  {
                'transporte' : remito.get_transporte_display(),
                'destinatario' : remito.destinatario.denominacion,
                'cuit' : remito.destinatario.cuit,
                'lugarEntrega': remito.lugarEntrega,
                'IVA' : remito.get_IVA_display(),
                'cantidad': remito.cantidad,
                'unidad' : remito.unidad,
                'producto' :  remito.producto, 
                'apellidoChofer' : remito.chofer.apellido,
                'nombreChofer' : remito.chofer.nombre,
                'dniChofer' : remito.chofer.dni,
                'marcaCamion' : remito.camion.marca,
                'patenteC' : remito.camion.patente,
                'marcaR' : remito.remolque.marca,
                'patenteR' : remito.remolque.patente,
                'observacion' : remito.observacion,
                'dia' : remito.fecha.day,
                'mes' : remito.fecha.month,
                'ano' : remito.fecha.year
                }
    
    doc.render(context)
    doc.save(response)
    return response



class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('cargarCamionesCsv/', self.admin_view(admin_cargarCamionesCsv_redirect), name='admin_cargarCamionesCsv')
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        # Agregar el enlace al menú de administración
        extra_context = extra_context or {}
        extra_context['custom_menu_links'] = [
            {
                'url': reverse('cargarCamionesCsv'),
                'name': 'CargarCamionesAFIP',
            }
        ]
        return super().index(request, extra_context)



admin_site = MyAdminSite(name='myadmin')
admin_site.register(Producto)
admin_site.register(AgenciaMaritima)
admin_site.register(Armadora)   
admin_site.register(Barco)
admin_site.register(Chofer)
admin_site.register(Cliente)
admin_site.register(Combustible)
admin_site.register(Configuracion)
admin_site.register(ContactoAgencia)
admin_site.register(Puerto)
admin_site.register(Transporte)

admin_site.site_header = 'Aplicacion OJR'
admin_site.register(Carga, CargaAdmin)
admin_site.register(Camion, CamionAdmin) 
admin_site.register(Remolque, RemolqueAdmin)
admin_site.register(RemitoVarios,RemitoVariosAdmin)
admin_site.register(ArmadoraPuerto, ArmadoraPuertoAdmin )

