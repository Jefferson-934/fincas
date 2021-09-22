from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'cedula', 
        'celular', 
        'email', 
        'type_user',
        'username',
        'create_at',
        'estado'
        )
    search_fields = ['cedula', 'username']

class FincaAdmin(admin.ModelAdmin):
    list_display =(
    'nombre_finca',
    'ubicacion' ,
    'latitud' ,
    'longitud' ,
    'propietario',
    )

    search_fields =['nombre_finca']
    


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Finca, FincaAdmin)
