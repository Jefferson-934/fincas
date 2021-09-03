from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Finca(models.Model):
    nombre_finca = models.CharField(max_length=150, unique=True)
    ubicacion = models.CharField(max_length=150)
    latitud = models.CharField(max_length=150)
    longitud = models.CharField(max_length=150)
    propietario = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='images/')
    create_at= models.DateTimeField(auto_now=True)
    estado=models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre_finca

class Cultivo(models.Model):
    nombre_lote = models.CharField(max_length=150)
    dimancion_lote = models.CharField(max_length=150)
    fecha_siembra = models.DateField()
    tiempo_cosecha = models.CharField(max_length=150)
    planta = models.ForeignKey('Planta', on_delete=models.CASCADE)
    finca = models.ForeignKey('Finca', on_delete=models.CASCADE)
    create_at= models.DateTimeField(auto_now=True)
    estado=models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_lote
   
class Planta(models.Model):
    nombre_planta = models.CharField(max_length=150, unique=True)
    nombre_cientifico = models.CharField(max_length=150)
    familia = models.CharField(max_length=150)
    genero = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='images/')
    create_at= models.DateTimeField(auto_now=True)
    estado=models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_planta


class Expediente(models.Model):
    finca = models.OneToOneField('Finca', on_delete=models.CASCADE, unique=True)
    propietario = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    direccion = models.CharField(max_length=150)
    total_cultivos = models.CharField(max_length=150)
    identificacion = models.CharField(max_length=150)
    plantas_existentes = models.CharField(max_length=150)
    total_plantas = models.CharField(max_length=150)  
    create_at= models.DateTimeField(auto_now=True)
    estado=models.BooleanField(default=False)



class CustomUser(AbstractUser):    
    cedula = models.CharField(max_length=10,unique=True)
    celular = models.CharField(max_length=10)
    email = models.EmailField(unique=True)    
    type_user = models.CharField(max_length=10)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email","cedula"]
    create_at= models.DateTimeField(auto_now=True)
    estado=models.BooleanField(default=False)

    

    def __str__(self):
        return self.username