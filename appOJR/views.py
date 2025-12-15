import decimal
import math
import os

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from appOJR.forms import (
    FormConfiguracion, FormAgenciaMaritima, FormPuerto, FormContactoAgencia, 
    FormCliente, FormTransporte, FormCamion, FormRemolque, FormProducto, 
    FormRancho, FormArmadora, FormChofer, CargaForm, RemitoForm, UploadCSVForm
)
from .models import (
    AgenciaMaritima, Armadora, Barco, Camion, Carga, Chofer, Cliente, 
    Combustible, Configuracion, ContactoAgencia, Producto, Puerto, Rancho, 
    Remito, RemitoVarios, Remolque, Transporte, ArmadoraPuerto
)
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin 
from django.http import HttpResponse
from django.template.loader import get_template
from docxtpl import DocxTemplate
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from .utils import actualizarCamionesDesdeCsv

# --- Vistas Generales ---

def index(request):
    return render(request, 'index.html')

def administracion(request):
    return render(request, 'admin')

# --- Helper Mixins ---

class BaseCRUD(SuccessMessageMixin):
    template_name_suffix = "" # Elimina el sufijo _form por defecto si se usa template_name

# --- BARCO ---

class BarcosListar(ListView): 
    template_name = "listarBarcos.html"
    model = Barco

class BarcoCrear(BaseCRUD, CreateView):
    template_name ="CrearBarco.html"
    model = Barco
    fields = "__all__"
    success_url = reverse_lazy('listarBarcos')
    success_message = "Barco creado correctamente"
    
class BarcoActualizar(BaseCRUD, UpdateView): 
    template_name ="CrearBarco.html"
    model = Barco
    fields = "__all__"
    success_url = reverse_lazy('listarBarcos')
    success_message = "Barco actualizado correctamente"

class BarcoEliminar(BaseCRUD, DeleteView): 
    model = Barco
    success_url = reverse_lazy('listarBarcos')
    success_message = "Barco eliminado correctamente"
    
class BarcoDetalle(DetailView): 
    model = Barco
    template_name = "appOJR/detallesBarco.html"


# --- CHOFER ---

class ChoferesListar(ListView): 
    template_name = "listarChoferes.html"
    model = Chofer

class ChoferCrear(BaseCRUD, CreateView):
    template_name ="CrearChofer.html"
    model = Chofer
    form_class = FormChofer
    success_url = reverse_lazy('listarChoferes')
    success_message = "Chofer creado correctamente"

class ChoferActualizar(BaseCRUD, UpdateView): 
    template_name ="CrearChofer.html"
    model = Chofer
    form_class = FormChofer
    success_url = reverse_lazy('listarChoferes')
    success_message = "Chofer actualizado correctamente"

class ChoferEliminar(BaseCRUD, DeleteView): 
    model = Chofer
    success_url = reverse_lazy('listarChoferes')
    success_message = "Chofer eliminado correctamente"

class ChoferDetalle(DetailView): 
    model = Chofer


# --- ARMADORA ---

class ArmadorasListar(ListView): 
    template_name = "listarArmadoras.html"
    model = Armadora

class ArmadoraCrear(BaseCRUD, CreateView):
    template_name ="CrearArmadora.html"
    model = Armadora
    form_class = FormArmadora
    success_url = reverse_lazy('listarArmadoras')
    success_message = "Armadora creada correctamente"

class ArmadoraActualizar(BaseCRUD, UpdateView): 
    template_name ="CrearArmadora.html"
    model = Armadora
    form_class = FormArmadora
    success_url = reverse_lazy('listarArmadoras')
    success_message = "Armadora actualizada correctamente"

class ArmadoraEliminar(BaseCRUD, DeleteView): 
    model = Armadora
    success_url = reverse_lazy('listarArmadoras')
    success_message = "Armadora eliminada correctamente"

class ArmadoraDetalle(DetailView): 
    model = Armadora


# --- AGENCIA MARITIMA ---

class AgenciaMaritimaListar(ListView):
    template_name = "listarAgenciasMaritimas.html"
    model = AgenciaMaritima

class AgenciaMaritimaCrear(BaseCRUD, CreateView):
    template_name = "CrearAgenciaMaritima.html"
    model = AgenciaMaritima
    form_class = FormAgenciaMaritima
    success_url = reverse_lazy('listarAgenciasMaritimas')
    success_message = "Agencia Marítima creada correctamente"

class AgenciaMaritimaActualizar(BaseCRUD, UpdateView):
    template_name = "CrearAgenciaMaritima.html"
    model = AgenciaMaritima
    form_class = FormAgenciaMaritima
    success_url = reverse_lazy('listarAgenciasMaritimas')
    success_message = "Agencia Marítima actualizada correctamente"

class AgenciaMaritimaEliminar(BaseCRUD, DeleteView):
    model = AgenciaMaritima
    success_url = reverse_lazy('listarAgenciasMaritimas')
    success_message = "Agencia Marítima eliminada correctamente"


# --- PUERTO ---

class PuertoListar(ListView):
    template_name = "listarPuertos.html"
    model = Puerto

class PuertoCrear(BaseCRUD, CreateView):
    template_name ="CrearPuerto.html"
    model = Puerto
    form_class = FormPuerto
    success_url = reverse_lazy('listarPuertos')
    success_message = "Puerto creado correctamente"

class PuertoActualizar(BaseCRUD, UpdateView):
    template_name ="CrearPuerto.html"
    model = Puerto
    form_class = FormPuerto
    success_url = reverse_lazy('listarPuertos')
    success_message = "Puerto actualizado correctamente"

class PuertoEliminar(BaseCRUD, DeleteView):
    model = Puerto
    success_url = reverse_lazy('listarPuertos')
    success_message = "Puerto eliminado correctamente"


# --- CONTACTO AGENCIA ---

class ContactoAgenciaListar(ListView):
    template_name = "listarContactosAgencia.html"
    model = ContactoAgencia

class ContactoAgenciaCrear(BaseCRUD, CreateView):
    template_name = "CrearContactoAgencia.html"
    model = ContactoAgencia
    form_class = FormContactoAgencia
    success_url = reverse_lazy('listarContactosAgencia')
    success_message = "Contacto creado correctamente"

class ContactoAgenciaActualizar(BaseCRUD, UpdateView):
    template_name = "CrearContactoAgencia.html"
    model = ContactoAgencia
    form_class = FormContactoAgencia
    success_url = reverse_lazy('listarContactosAgencia')
    success_message = "Contacto actualizado correctamente"

class ContactoAgenciaEliminar(BaseCRUD, DeleteView):
    model = ContactoAgencia
    success_url = reverse_lazy('listarContactosAgencia')
    success_message = "Contacto eliminado correctamente"


# --- CLIENTE ---

class ClienteListar(ListView):
    template_name = "listarClientes.html"
    model = Cliente

class ClienteCrear(BaseCRUD, CreateView):
    template_name = "CrearCliente.html"
    model = Cliente
    form_class = FormCliente
    success_url = reverse_lazy('listarClientes')
    success_message = "Cliente creado correctamente"

class ClienteActualizar(BaseCRUD, UpdateView):
    template_name = "CrearCliente.html"
    model = Cliente
    form_class = FormCliente
    success_url = reverse_lazy('listarClientes')
    success_message = "Cliente actualizado correctamente"

class ClienteEliminar(BaseCRUD, DeleteView):
    model = Cliente
    success_url = reverse_lazy('listarClientes')
    success_message = "Cliente eliminado correctamente"


# --- TRANSPORTE ---

class TransporteListar(ListView):
    template_name = "listarTransportes.html"
    model = Transporte

class TransporteCrear(BaseCRUD, CreateView):
    template_name = "CrearTransporte.html"
    model = Transporte
    form_class = FormTransporte
    success_url = reverse_lazy('listarTransportes')
    success_message = "Transporte creado correctamente"

class TransporteActualizar(BaseCRUD, UpdateView):
    template_name = "CrearTransporte.html"
    model = Transporte
    form_class = FormTransporte
    success_url = reverse_lazy('listarTransportes')
    success_message = "Transporte actualizado correctamente"

class TransporteEliminar(BaseCRUD, DeleteView):
    model = Transporte
    success_url = reverse_lazy('listarTransportes')
    success_message = "Transporte eliminado correctamente"


# --- CAMION ---

class CamionListar(ListView):
    template_name = "listarCamiones.html"
    model = Camion

class CamionCrear(BaseCRUD, CreateView):
    template_name ="CrearCamion.html"
    model = Camion
    form_class = FormCamion
    success_url = reverse_lazy('listarCamiones')
    success_message = "Camión creado correctamente"

class CamionActualizar(BaseCRUD, UpdateView):
    template_name ="CrearCamion.html"
    model = Camion
    form_class = FormCamion
    success_url = reverse_lazy('listarCamiones')
    success_message = "Camión actualizado correctamente"

class CamionEliminar(BaseCRUD, DeleteView):
    model = Camion
    success_url = reverse_lazy('listarCamiones')
    success_message = "Camión eliminado correctamente"


# --- REMOLQUE ---

class RemolqueListar(ListView):
    template_name = "listarRemolques.html"
    model = Remolque

class RemolqueCrear(BaseCRUD, CreateView):
    template_name = "CrearRemolque.html"
    model = Remolque
    form_class = FormRemolque
    success_url = reverse_lazy('listarRemolques')
    success_message = "Remolque creado correctamente"

class RemolqueActualizar(BaseCRUD, UpdateView):
    template_name = "CrearRemolque.html"
    model = Remolque
    form_class = FormRemolque
    success_url = reverse_lazy('listarRemolques')
    success_message = "Remolque actualizado correctamente"

class RemolqueEliminar(BaseCRUD, DeleteView):
    model = Remolque
    success_url = reverse_lazy('listarRemolques')
    success_message = "Remolque eliminado correctamente"


# --- PRODUCTO ---

class ProductoListar(ListView):
    template_name = "listarProductos.html"
    model = Producto

class ProductoCrear(BaseCRUD, CreateView):
    template_name = "CrearProducto.html"
    model = Producto
    form_class = FormProducto
    success_url = reverse_lazy('listarProductos')
    success_message = "Producto creado correctamente"

class ProductoActualizar(BaseCRUD, UpdateView):
    template_name = "CrearProducto.html"
    model = Producto
    form_class = FormProducto
    success_url = reverse_lazy('listarProductos')
    success_message = "Producto actualizado correctamente"

class ProductoEliminar(BaseCRUD, DeleteView):
    model = Producto
    success_url = reverse_lazy('listarProductos')
    success_message = "Producto eliminado correctamente"


# --- RANCHO ---

class RanchoListar(ListView):
    template_name = "listarRanchos.html"
    model = Rancho

class RanchoCrear(BaseCRUD, CreateView):
    template_name = "CrearRancho.html"
    model = Rancho
    form_class = FormRancho
    success_url = reverse_lazy('listarRanchos')
    success_message = "Rancho creado correctamente"

class RanchoActualizar(BaseCRUD, UpdateView):
    template_name = "CrearRancho.html"
    model = Rancho
    form_class = FormRancho
    success_url = reverse_lazy('listarRanchos')
    success_message = "Rancho actualizado correctamente"

class RanchoEliminar(BaseCRUD, DeleteView):
    model = Rancho
    success_url = reverse_lazy('listarRanchos')
    success_message = "Rancho eliminado correctamente"

# --- COMBUSTIBLE ---

class CombustibleListar(ListView):
    template_name = "listarCombustibles.html"
    model = Combustible

class CombustibleCrear(BaseCRUD, CreateView):
    template_name ="CrearCombustible.html"
    model = Combustible 
    fields = "__all__"
    success_url = reverse_lazy('listarCombustibles')
    success_message = "Combustible creado correctamente"

class CombustibleActualizar(BaseCRUD, UpdateView):
    template_name ="CrearCombustible.html"
    model = Combustible 
    fields = "__all__"
    success_url = reverse_lazy('listarCombustibles')
    success_message = "Combustible actualizado correctamente"

class CombustibleEliminar(BaseCRUD, DeleteView):
    model = Combustible
    success_url = reverse_lazy('listarCombustibles')
    success_message = "Combustible eliminado correctamente"


# --- CARGA ---

class CargaListar(ListView):
    queryset = Carga.objects.order_by('-fechaInicio')
    template_name = "listarCargas.html"

class CargaCrear(BaseCRUD, CreateView):
    template_name ="CrearCarga.html"
    model = Carga
    fields = "__all__"
    success_url = reverse_lazy('listarCargas')
    success_message = "Carga creada correctamente"
    
class CargaRemito(BaseCRUD, CreateView):
    model = Carga
    fields = ['barco', 'puerto', 'combustible', 'sitioPuerto']
    template_name = 'CrearCargaRemito.html'
    success_url = reverse_lazy('listarCargas')
    success_message = "Carga creada correctamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['camiones'] = Camion.objects.all()
        context['choferes'] = Chofer.objects.all()
        context['remolques'] = Remolque.objects.all()
        return context
    
class CargaActualizar(BaseCRUD, UpdateView): 
    template_name ="CrearCarga.html"
    model = Carga
    fields = "__all__"
    success_url = reverse_lazy('listarCargas')
    success_message = "Carga actualizada correctamente"

class CargaEliminar(BaseCRUD, DeleteView): 
    model = Carga
    success_url = reverse_lazy('listarCargas')
    success_message = "Carga eliminada correctamente"

class CargaDetalle(DetailView): 
    model = Carga


# --- REMITO ---

class RemitosListar(ListView):
    queryset = Remito.objects.all()
    template_name = "listarRemitos.html"

class RemitoCombustibleCrear(BaseCRUD, CreateView):
    template_name ="CrearRemitoCombustible.html"
    model = Remito
    fields = "__all__"
    success_url = reverse_lazy('listarRemitos')
    success_message = "Remito Combustible creado correctamente"

class RemitoVariosCrear(BaseCRUD, CreateView):
    template_name ="CrearRemitoVarios.html"
    model = RemitoVarios
    fields = "__all__"
    success_url = reverse_lazy('listarRemitos')
    success_message = "Remito Varios creado correctamente"

class RemitoActualizar(BaseCRUD, UpdateView): 
    template_name ="CrearRemitoCombustible.html"
    model = Remito
    fields = "__all__"
    success_url = reverse_lazy('listarRemitos')
    success_message = "Remito actualizado correctamente"

class RemitoEliminar(BaseCRUD, DeleteView): 
    model = Remito
    success_url = reverse_lazy('listarRemitos')
    success_message = "Remito eliminado correctamente"

class RemitoDetalle(DetailView): 
    model = Remito


# --- CONFIGURACION y OTROS ---

class ConfiguracionPantalla(SuccessMessageMixin, UpdateView): 
    template_name ="Configuracion.html"
    model = Configuracion
    fields = "__all__"
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

def CerrarSesion(request):
    return render(request, 'logout.html')

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


# --- AJAX Vistas ---

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


# --- GENERACION DE DOCUMENTOS (Sin Cambios) ---

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
