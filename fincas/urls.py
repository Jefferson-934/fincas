from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from fincas.core import views

urlpatterns = [
    

    
    path('login/', views.loginu, name='login'),
    path('logout/', views.cerrar, name='logout'),
    path('', views.home, name='home'),
    #Usuarios
    path('usuarios/', views.usuarios, name='usuarios'),
    path('nuevo_usuarios/', views.new_usuarios, name='nuevo_usuarios'),
    path('delete_usuario/<id>/', views.delete_usuario, name='delete_usuario'),
    path('actualizar_usuario/<id>/', views.actualizar_usuario, name='actualizar_usuario'),
    path('activar_usuario/<id>/', views.activar_usuario, name='activar_usuario'),


    #plantas
    path('plantas/', views.plantas, name='plantas'),
    path('nuevo_planta/', views.new_planta, name='nuevo_planta'),
    path('delete_planta/<id>/', views.delete_planta, name='delete_planta'),
    path('actualizar_planta/<id>/', views.actualizar_planta, name='actualizar_planta'),

    #cultivos
    path('cultivos/', views.cultivos, name='cultivos'),
    path('nuevo_cultivo/', views.new_cultivo, name='nuevo_cultivo'),
    path('actualizar_cultivo/<id>/', views.actualizar_cultivo, name='actualizar_cultivo'),
    path('delete_cultivo/<id>/', views.delete_cultivo, name='delete_cultivo'),
     path('datos_estadisticos/', views.estadistica_cultivo, name='datos_estadisticos'),
    path('retonarCultivos/', views.retonarCultivos, name='retonarCultivos'),




    #fincas
    path('fincas/', views.fincas, name='fincas'),
    path('perfil_fincas/<id>/', views.perfil_fincas, name='perfil_fincas'),
    path('nuevo_finca/', views.new_finca, name='nuevo_finca'),
    path('actualizar_finca/<id>/', views.actualizar_finca, name='actualizar_finca'),
    path('delete_finca/<id>/', views.delete_finca, name='delete_finca'),
    path('activar_finca/<id>/', views.activar_finca, name='activar_finca'),


    #Expediente
    path('expedientes/', views.expedientes, name='expedientes'),
    path('nuevo_expediente/', views.new_expediente, name='nuevo_expediente'),
    path('actualizar_expediente/<id>/', views.actualizar_expediente, name='actualizar_expediente'),
    path('delete_expediente/<id>/', views.delete_expediente, name='delete_expediente'),


    path('obtener_datos/', views.obtener_datos, name='obtener_datos'),
  
    path('admin/', admin.site.urls),


    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
