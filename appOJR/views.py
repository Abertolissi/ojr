import decimal
import math
import os

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from appOJR.forms import FormConfiguracion
from .models import AgenciaMaritima, Armadora, Barco, Camion, Carga, Chofer, Combustible, Configuracion,Puerto, Remito, RemitoVarios, Remolque
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin 
from django.http import HttpResponse
from django.template.loader import get_template
from docxtpl import DocxTemplate
from .forms import CargaForm, RemitoForm
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required




#Para obtener todos los registros de la tabla Barcos

def index(request):
    return render(request, 'index.html')

def administracion(request):
    return render(request, 'admin')


# BARCO

#Para insertar un nuevo Barco en la tabla Barcos 

class BarcoCrear(CreateView):
    template_name ="CrearBarco.html"
    model = Barco
    fields = "__all__"
    def get_success_url(self):
        # Mensaje que se mostrará cuando se 
        return reverse('listarBarcos')
    
#Para modificar un Barco existente de la tabla Barcos
class BarcoActualizar(SuccessMessageMixin, UpdateView): 
    template_name ="CrearBarco.html"
    model = Barco
    form = Barco
    fields = "__all__"
   
    # Redireccionamos a la página principal tras actualizar el registro
    def get_success_url(self):
        return reverse('listarBarcos')

#Para eliminar un Barco de la tabla Barcos 
class BarcoEliminar(SuccessMessageMixin, DeleteView): 
    model = Barco
    form = Barco
    fields = "__all__"     
 
    #Redireccionamos a la página principal tras de eliminar el registro
    def get_success_url(self):
        # Mensaje que se mostrará cuando se elimine el registro
        success_message = 'Barco eliminado correctamente.'
        messages.success (self.request, (success_message))       
        return reverse('listarBarcos')
    
class BarcosListar(ListView): 
    template_name = "listarBarcos.html"
    model = Barco

#Para obtener todos los campos de un registro de la tabla Barcos 
class BarcoDetalle(DetailView): 
    model = Barco


#CHOFER 

#Para insertar un nuevo Chofer en la tabla Choferes

class ChoferCrear(CreateView):
    template_name ="CrearChofer.html"
    model = Chofer
    fields = "__all__"
    def get_success_url(self):
        # Mensaje que se mostrará cuando se 
        return reverse('listarChoferes')
    
 
#Para modificar un Chofer existente de la tabla Choferes
class ChoferActualizar(SuccessMessageMixin, UpdateView): 
    template_name ="CrearChofer.html"
    model = Chofer
    form = Chofer
    fields = "__all__"
    
    # Redireccionamos a la página principal tras actualizar el registro
    def get_success_url(self):
        return reverse('listarChoferes')

#Para eliminar un Chofer de la tabla Choferes
class ChoferEliminar(SuccessMessageMixin, DeleteView): 
    model = Chofer
    form = Chofer
    fields = "__all__"     
 
    #Redireccionamos a la página principal tras de eliminar el registro
    def get_success_url(self):
        # Mensaje que se mostrará cuando se elimine el registro
        success_message = 'Chofer eliminado correctamente.'
        messages.success (self.request, (success_message))       
        return reverse('listarChoferes')
    
class ChoferesListar(ListView): 
    template_name = "listarChoferes.html"
    model = Chofer

class ChoferDetalle(DetailView): 
    model = Chofer



#ARMADORA

class ArmadoraCrear(CreateView):
    template_name ="CrearArmadora.html"
    model = Armadora
    fields = "__all__"
    
    # Redirigimos a la página principal tras insertar el registro
    def get_success_url(self):        
        return reverse('listarArmadoras')

#Para modificar un Armadora existente de la tabla Armadora
class ArmadoraActualizar(SuccessMessageMixin, UpdateView): 
    template_name ="CrearArmadora.html"
    model = Armadora
    fields = "__all__"
  
    # Redireccionamos a la página principal tras actualizar el registro
    def get_success_url(self):
        return reverse('listarArmadoras')

#Para eliminar una Armadora de la tabla Armadoras 
class ArmadoraEliminar(SuccessMessageMixin, DeleteView): 
    model = Armadora
    form = Armadora
    fields = "__all__"     
 
    #Redireccionamos a la página principal tras de eliminar el registro
    def get_success_url(self):
        # Mensaje que se mostrará cuando se elimine el registro
        success_message = 'Armadora eliminado correctamente.'
        messages.success (self.request, (success_message))       
        return reverse('listarArmadoras')
    
class ArmadorasListar(ListView): 
    template_name = "listarArmadoras.html"
    model = Armadora

class ArmadoraDetalle(DetailView): 
    model = Armadora

#CARGA
 
class CargaCrear(CreateView):
    template_name ="CrearCarga.html"
    model = Carga
    fields = "__all__"
    def get_success_url(self):
        # Mensaje que se mostrará cuando se 
        success_message = 'Carga creada correctamente.'
        messages.success (self.request, (success_message))       
        return reverse('listarCargas')
    
class CargaRemito(CreateView):

    model = Carga
    fields = ['barco', 'puerto', 'combustible', 'sitioPuerto']
    template_name = 'CrearCargaRemito.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener las listas de camiones, choferes y remolques de la base de datos
        context['camiones'] = Camion.objects.all()
        context['choferes'] = Chofer.objects.all()
        context['remolques'] = Remolque.objects.all()
        return context
    
    def get_success_url(self):
        # Mensaje que se mostrará cuando se carga correctamente
        success_message = 'Carga creada correctamente.'
        messages.success (self.request, (success_message))       
        return reverse('listarCargas')  
    
    
#Para modificar un Carga existente de la tabla Cargas
class CargaActualizar(SuccessMessageMixin, UpdateView): 
    template_name ="CrearCarga.html"
    model = Carga
    fields = "__all__"
    # Mensaje que se mostrará cuando se actualice el registro
    success_message = 'Carga actualizado correctamente.'
 
    # Redireccionamos a la página principal tras actualizar el registro
    def get_success_url(self):
        return reverse('listarCargas')


#Para eliminar una Armadora de la tabla Armadoras 
class CargaEliminar(SuccessMessageMixin, DeleteView): 
    model = Carga
    form = Carga
    fields = "__all__"     
 
    #Redireccionamos a la página principal tras de eliminar el registro
    def get_success_url(self):
        # Mensaje que se mostrará cuando se elimine el registro
        success_message = 'Carga eliminada correctamente.'
        messages.success (self.request, (success_message))       
        return reverse('listarCargas')

class CargaListar(ListView):
    queryset = Carga.objects.order_by('-fechaInicio')
    template_name = "listarCargas.html"
    #model = Carga

class CargaDetalle(DetailView): 
    model = Carga

#REMITO
 
class RemitoCombustibleCrear(CreateView):
    template_name ="CrearRemitoCombustible.html"
    model = Remito
    fields = "__all__"
    def get_success_url(self):
        # Mensaje que se mostrará cuando se 
        success_message = 'Remito creado correctamente.'
        messages.success (self.request, (success_message))       
        return reverse('listarRemitos')

class RemitoVariosCrear(CreateView):
    template_name ="CrearRemitoVarios.html"
    model = RemitoVarios
    fields = "__all__"
    def get_success_url(self):
        # Mensaje que se mostrará cuando se 
        success_message = 'Remito creado correctamente.'
        messages.success (self.request, (success_message))       
        return reverse('listarRemitos')
    


#Para modificar un Remito existente de la tabla Remitos
class RemitoActualizar(SuccessMessageMixin, UpdateView): 
    template_name ="CrearRemitoCombustible.html"
    model = Remito
    fields = "__all__"
    # Mensaje que se mostrará cuando se actualice el registro
    success_message = 'Remito actualizado correctamente.'
 
    # Redireccionamos a la página principal tras actualizar el registro
    def get_success_url(self):
        return reverse('listarRemitos')


#Para eliminar un remito de Remitos
class RemitoEliminar(SuccessMessageMixin, DeleteView): 
    model = Remito
    form = Remito
    fields = "__all__"     
 
    #Redireccionamos a la página principal tras de eliminar el registro
    def get_success_url(self):
        # Mensaje que se mostrará cuando se elimine el registro
        success_message = 'Remito eliminado correctamente.'
        messages.success (self.request, (success_message))       
        return reverse('listarRemitos')

class RemitosListar(ListView):
    # queryset = Remito.objects.order_by('-fecha')
    queryset = Remito.objects.all()
    template_name = "listarRemitos.html"
    
class RemitoDetalle(DetailView): 
    model = Remito

#VISTAS VARIAS


class PuertoCrear(CreateView):
    template_name ="CrearPuerto.html"
    model = Puerto
    fields = "__all__"

    def get_success_url(self):
        return reverse('index' )

class CamionCrear(CreateView):
    template_name ="CrearCamion.html"
    model = Camion
    fields = "__all__"

    def get_success_url(self):
        return reverse('index' )

class CombustibleCrear(CreateView):
    template_name ="CrearCombustible.html"
    model = Combustible 
    fields = "__all__"

    def get_success_url(self):
        return reverse('index' )
    
class AgenciaMaritimaCrear(CreateView):
    template_name ="CrearAgenciaMaritima.html"
    model = AgenciaMaritima
    fields = "__all__"

    def get_success_url(self):
        return reverse('index' )
    
def getCamiones(request):
    transporte_id = request.GET.get('transporte_id')
    camiones = Camion.objects.filter(transporte_id=transporte_id,habilitadoAFIP=True).values_list('id', 'patente')
    camiones_dict = dict(camiones)
    return JsonResponse({'camiones': camiones_dict})

def getRemolques(request):
    transporte_id = request.GET.get('transporte_id')
    remolques = Remolque.objects.filter(transporte_id=transporte_id).values_list('id', 'patente')
    remolques_dict = dict(remolques)
    return JsonResponse({'remolques': remolques_dict})

#Para modificar la configuracion
class ConfiguracionPantalla(SuccessMessageMixin, UpdateView): 
    template_name ="Configuracion.html"
    model = Configuracion
    fields = "__all__"
    # Redireccionamos a la página principal tras actualizar el registro
    def get_success_url(self):
        return reverse('index')
    
def formConfiguracion(request):
    form = FormConfiguracion(request.POST or None)
    if form.is_valid():
        form.save()		
        form = FormConfiguracion()
    else:
        messages.error(request, 'Error al insertar Configuracion. Revise los datos.')
    context = {'form': form }      
    return render(request, 'Configuracion.html', context)

#Ejemplo de redirección a una página HTML existente
def CerrarSesion(request):
    return render(request, 'logout.html')

def generarRemitoCombustible(request,idRemito, impresora):
       
    remito = Remito.objects.get(id=idRemito )
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename="RemitoNro"' + str(remito.numero) + '".docx"'
    if (impresora ==  "brother"):
        doc = DocxTemplate(os.getcwd() + '/appOJR/templates/RemitoBrother.docx')
    else:    
        doc = DocxTemplate(os.getcwd() + '/appOJR/templates/RemitoLaser.docx')
    densidad = remito.densidad*1000
    factor1 =(decimal.Decimal(346.4228)/(densidad**2))+(decimal.Decimal(0.4388)/densidad)
    factor2 =decimal.Decimal(-0.00336312) +(decimal.Decimal(2680.3206)/densidad**2)
    factor3 = (decimal.Decimal(594.5418)/(densidad**2))
    factor4= (decimal.Decimal(186.9696)/(densidad**2))+(decimal.Decimal(0.4862)/densidad)

    
    if (densidad <decimal.Decimal(770.8)):
        VCF = round(math.exp(-factor1*(remito.temperatura-15)*(1+decimal.Decimal(0.8)*factor1*(remito.temperatura-15))),5)
    elif (densidad <decimal.Decimal(787.5)):      
        VCF = round(math.exp(-factor2*(remito.temperatura-15)*(1+decimal.Decimal(0.8)*factor2*(remito.temperatura-15))),5)
    elif (densidad <decimal.Decimal(832.3)):      
        VCF = round(math.exp(-factor3*(remito.temperatura-15)*(1+decimal.Decimal(0.8)*factor3*(remito.temperatura-15))),5)
    else:
        VCF = round(math.exp(-factor4*(remito.temperatura-15)*(1+decimal.Decimal(0.8)*factor4*(remito.temperatura-15))),5)   

    configuracion  = Configuracion.objects.get(id=1)
    context =  {
                 'armadora' : remito.barco.armadora.nombre,
                'barco' : remito.barco.nombre,
                'puerto' : remito.puerto.nombre,
                'cuitArmadora' : remito.barco.armadora.cuit,
                'combustible' : remito.combustible.nombre,
                'apellidoChofer' : remito.chofer.apellido,
                'nombreChofer' : remito.chofer.nombre,
                'dniChofer' : remito.chofer.dni,
                'marcaCamion' : remito.camion.marca,
                'patenteC' : remito.camion.patente,
                'marcaR' : remito.remolque.marca,
                'patenteR' : remito.remolque.patente,
                'cantidadTotal' :math.trunc((remito.cantidadBarco + remito.cantidadDeposito) * 1000 * VCF),
                'cantidadBarco' :math.trunc((remito.cantidadBarco * 1000 *VCF)),
                'cantidadDeposito' :math.trunc(remito.cantidadDeposito * 1000 * VCF),
                'fc' : VCF,
                'azufre' : '<<300',
                'den' :remito.densidad ,
                'temp' :remito.temperatura ,
                'marcaR' : remito.remolque.marca,
                'patenteR' : remito.remolque.patente,
                'dia' : remito.fecha.day,
                'mes' : remito.fecha.month,
                'ano' : remito.fecha.year
                }
    doc.render(context)
    doc.save(response)
    return response

def generarRemitoVarios(request,idRemito, impresora):
       
    remito = RemitoVarios.objects.get(id=idRemito )
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename="RemitoNro"' + str(remito.numero) + '".docx"'
    if (impresora ==  "brother"):
        doc = DocxTemplate(os.getcwd() + '/appOJR/templates/RemitoBrother.docx')
    else:    
        doc = DocxTemplate(os.getcwd() + '/appOJR/templates/RemitoLaser.docx')
    
    configuracion  = Configuracion.objects.get(id=1)
    context =  {
                'apellidoChofer' : remito.chofer.apellido,
                'nombreChofer' : remito.chofer.nombre,
                'dniChofer' : remito.chofer.dni,
                'marcaCamion' : remito.camion.marca,
                'patenteC' : remito.camion.patente,
                'marcaR' : remito.remolque.marca,
                'patenteR' : remito.remolque.patente,
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

def generarDocumento(request,idCarga):
       
    carga = Carga.objects.get(id=idCarga )
    if carga.puerto.nombre== 'Camarones':
        response=generarDocumentosCamarones(idCarga);
    elif carga.puerto.nombre== 'Puerto Madryn':
        response= generarDocumentosPuertoMadryn(idCarga);
    else:
        response=generarDocumentosRawson(idCarga);
    return response


def generarDocumentosCamarones(idCarga):

    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename="Formularios-Camarones.docx"'

    doc = DocxTemplate(os.getcwd() + '/appOJR/templates/Formularios-Camarones.docx')
  
    carga = Carga.objects.get(id=idCarga)
    configuracion  = Configuracion.objects.get(id=1)
    context =  {'barco' : carga.barco.nombre,
                'bandera' : carga.barco.bandera,
                'armadora' : carga.barco.armadora.nombre,
                'matricula' : carga.barco.matricula,
                'apellidoChofer' : carga.chofer.apellido,
                'nombreChofer' : carga.chofer.nombre,
                'dniChofer' : carga.chofer.dni,
                'pnaChofer' :carga.chofer.pna,
                'empresa' : configuracion.empresa,
                'domicilioEmpresa' : configuracion.direccionEmpresa,
                'titularEmpresa' : configuracion.titularEmpresa,
                'cuitEmpresa' : configuracion.cuitEmpresa,
                'telefonoEmpresa' : configuracion.telefonoEmpresa,
                'emailEmpresa' : configuracion.emailEmpresa,
                'certificadoInscripcion' : configuracion.certificadoInscripcion,
                'vencimientoCertificadoInscripcion' : configuracion.vencimientoCertificadoInscripcion.strftime("%d/%m/%Y"),
                'patenteCamion' :carga.camion.patente,
                'patenteRemolque' :carga.patenteRemolque,
                'cantidad' :carga.cantidad * 1000,
                'aseguradoraChoferes' :configuracion.aseguradoraChoferes,
                'vencimientoAseguradora' :configuracion.vencimientoAseguradora.strftime("%d/%m/%Y"),
                'fechaInicio' : carga.fechaInicio.strftime("%d/%m/%Y"),
                'horaInicio' : carga.horaInicio.strftime("%H:%M")}
    doc.render(context)
    doc.save(response)
    return response
    

def generarDocumentosPuertoMadryn(idCarga):
  
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename="Formularios-PuertoMadryn.docx"'

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
                'cantidad' :carga.cantidad,
                'cantidadCamiones' : carga.cantCamiones,
                'vencimientoCertificadoInscripcion' : configuracion.vencimientoCertificadoInscripcion.strftime("%d/%m/%Y"),
                'fechaInicio' : carga.fechaInicio.strftime("%d/%m/%Y")
    }
    doc.render(context)
    doc.save(response)
    return response


def generarDocumentosRawson(idCarga):
    
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename="Formularios-Rawson.docx"'

    doc = DocxTemplate(os.getcwd() + '/appOJR/templates/Formularios-Rawson.docx')
  
    carga = Carga.objects.get(id=idCarga )
    configuracion  = Configuracion.objects.get(id=1)
    context =  {'empresa' : configuracion.empresa, 
                'armadora' : carga.barco.armadora.nombre, 
                'telefonoArmadora' : carga.barco.armadora.telefono, 
                'matricula' : carga.barco.matricula,
                'apellidoChofer' : carga.chofer.apellido,
                'nombreChofer' : carga.chofer.nombre,
                'dniChofer' : carga.chofer.dni,
                'pnaChofer' :carga.chofer.pna,
                'telefonoChofer' :carga.chofer.telefono,
                'nacionalidadChofer' :carga.chofer.nacionalidad,
                'domicilioChofer' :carga.chofer.domicilio,
                'barco' : carga.barco.nombre,
                'eslora' : '{0:.3g}'.format(carga.barco.eslora).replace(",", "@").replace(".", ",").replace("@", "."),
                'manga' : '{0:.3g}'.format(carga.barco.manga).replace(",", "@").replace(".", ",").replace("@", "."),
                'puntal' :  '{0:.3g}'.format(carga.barco.puntal).replace(",", "@").replace(".", ",").replace("@", "."),
                'marcaCamion' : carga.camion.marca,
                'patenteCamion' : carga.camion.patente,
                'sitioPuerto' :carga.sitioPuerto,
                'empresa' : configuracion.empresa,
                'titularEmpresa' : configuracion.titularEmpresa,
                'cuitEmpresa' : configuracion.cuitEmpresa,
                'tipoCombustible' : carga.combustible.nombre,
                'cantidad' :carga.cantidad*1000,
                'cantidadCamiones' : carga.cantCamiones,
                'fechaInicio' : carga.fechaInicio.strftime("%d/%m/%Y"),
                'horaInicio' : carga.horaInicio.strftime("%H:%M")}
    doc.render(context)
    doc.save(response)
    return response

from .forms import UploadCSVForm
from .utils import actualizarCamionesDesdeCsv

def cargarCamionesView(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            actualizarCamionesDesdeCsv(csv_file)
            messages.success(request, 'Los camiones han sido actualizados correctamente.')
            return redirect('upload_csv')
    else:
        form = UploadCSVForm()
    return render(request, 'cargarCamionesAFIP.html', {'form': form})


@staff_member_required
def admin_cargarCamionesCsv_redirect(request):
    return redirect('cargarCamionesCsv')


