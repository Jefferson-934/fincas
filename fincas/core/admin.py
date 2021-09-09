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
    


admin.site.register(CustomUser, CustomUserAdmin)
