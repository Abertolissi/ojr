from django import forms
from .models import Barco, Carga, Combustible, Configuracion, Remito

class FormCrearBarco(forms.ModelForm):

    class Meta:
        model = Barco
        fields = '__all__'
       
class FormCrearCarga(forms.ModelForm):
    
    class Meta:
        model = Carga
        fields = '__all__'
        widgets = {
            'fechaHoraInicio': forms.DateTimeInput(
                attrs={'type': 'Datetime-local', 'class': 'form-control'}
            )
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
        fields = '__all__'  # Para incluir todos los campos del modelo

class RemitoForm(forms.ModelForm):
    class Meta:
        model = Remito
        fields = ['transporte', 'numero', 'chofer', 'remolque', 'camion', 'cantidadBarco', 'cantidadDeposito']

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()

