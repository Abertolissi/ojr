from django import forms
from .models import (
    AgenciaMaritima, Armadora, ArmadoraPuerto, Barco, Camion, Carga, Chofer, 
    Cliente, Combustible, Configuracion, ContactoAgencia, Producto, Puerto, 
    Rancho, Remito, RemitoVarios, Remolque, Transporte
)

class FormCrearBarco(forms.ModelForm):
    class Meta:
        model = Barco
        fields = '__all__'
       
class FormCrearCarga(forms.ModelForm):
    class Meta:
        model = Carga
        fields = '__all__'
        widgets = {
            'fechaInicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horaInicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        
class DateInput(forms.DateInput):
    input_type = 'date' 

class FormCombustible(forms.ModelForm):
    class Meta:
        model = Combustible
        fields = '__all__'

class FormConfiguracion(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = '__all__'

class CargaForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = '__all__' 

class RemitoForm(forms.ModelForm):
    class Meta:
        model = Remito
        fields = ['transporte', 'numero', 'chofer', 'remolque', 'camion', 'cantidadBarco', 'cantidadDeposito']

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()

# Nuevos Forms

class FormAgenciaMaritima(forms.ModelForm):
    class Meta:
        model = AgenciaMaritima
        fields = '__all__'

class FormPuerto(forms.ModelForm):
    class Meta:
        model = Puerto
        fields = '__all__'

class FormContactoAgencia(forms.ModelForm):
    class Meta:
        model = ContactoAgencia
        fields = '__all__'

class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class FormTransporte(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = '__all__'

class FormCamion(forms.ModelForm):
    class Meta:
        model = Camion
        fields = '__all__'

class FormRemolque(forms.ModelForm):
    class Meta:
        model = Remolque
        fields = '__all__'

class FormProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class FormRancho(forms.ModelForm):
    class Meta:
        model = Rancho
        fields = '__all__'
        widgets = {
            'fechaCarga': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class FormArmadora(forms.ModelForm):
    class Meta:
        model = Armadora
        fields = '__all__'

class FormChofer(forms.ModelForm):
    class Meta:
        model = Chofer
        fields = '__all__'
