from django import forms
from fincas.core.models import *

class LoginForms(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username","password")



class RegisterUserForms(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username","password","cedula","first_name","email","celular")

class UpdateUserForms(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username","cedula","first_name","email","celular")


class RegisterPantaForms(forms.ModelForm):
    class Meta:
        model = Planta
        fields = ("nombre_planta","nombre_cientifico","familia","genero","imagen")


class RegisterCultivoForms(forms.ModelForm):
    class Meta:
        model = Cultivo
        fields = ("nombre_lote","dimancion_lote","fecha_siembra","tiempo_cosecha","planta","finca")


class RegisterExpedientesForms(forms.ModelForm):
    class Meta:
        model = Expediente
        fields = ("finca","propietario","direccion","total_cultivos","identificacion","plantas_existentes","total_plantas")



class RegisterFincasForms(forms.ModelForm):
    class Meta:
        model = Finca
        fields = ("nombre_finca","ubicacion","latitud","longitud","propietario","imagen")