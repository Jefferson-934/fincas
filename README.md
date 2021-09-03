# Registro de Fincas

__

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **Deployment** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

_Vamos a necesitar todas la librerias que se encuentran en el archivo requirements.txt_
_antes de instalar las librerias se debe crear un entonor virtual al nivel de la carpeta del proyecto_

_Creación de entorno virtual con python 3.8 o superior_

```
python -m venv entorno
```

_Activando entorno virtual para levantar el proyecto en windows_
_iniciar cmd en carpeta general del proyecto y del entorno_
```
"entorno/Scripts/activate"
```

### Instalación 🔧

_una vez levantado el entorno virtual debemos acceder a la carpeta donde se encuentra el archivo manage.py junto al archivo requirements.txt_

_Instalar librerias_

```
pip install -r requirements.txt
```


## Ejecutando las pruebas ⚙️

_Una vez realizado los pasos anteriores debemos ejecutar las migraciones_
```
python manage.py makemigrations
```
_Ejecutar migracion a la base de datos_
```
python manage.py migrate
```
_Crear usuario administrador desde la consola para hacer el login en la aplicacion como administrador_
```
python manage.py createsuperuser
```
## Despliegue 📦

_Para levantar el proyecto debemos ejecutar_
```
python manage.py runserver
```