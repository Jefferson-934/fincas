
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from fincas.core.forms import *
from fincas.core.models import *
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import get_object_or_404
import django_excel as exel
from datetime import datetime
from django.http import HttpResponse, response
from excel_response import ExcelResponse
from django.contrib import messages
import json as simplejson
import random 


def cerrar(request):
    logout(request)
    return redirect('login')


def loginu(request):
    print(request.method)
    form = LoginForms(data=request.POST)
    if request.method == 'POST':
        print("entro")        
        username = request.POST.get('username',"")
        password = request.POST.get('password',"")           
        users = authenticate(username=username, password=password)
        print(users)
        if users is not None:
            print(users)
            login(request, users)
            if users.is_staff:
                return redirect('fincas')
            else:
                return redirect('perfil_fincas',id=users.pk)
        else:
            return render(request, 'registration/login.html',{"error":"Datos incorrectos"})
        
    return render(request, 'registration/login.html')



def verificar_cedula(nro):
    l = len(nro)
    if l == 10 or l == 13: # verificar la longitud correcta
        cp = int(nro[0:2])
        if cp >= 1 and cp <= 22: # verificar codigo de provincia
            tercer_dig = int(nro[2])
            if tercer_dig >= 0 and tercer_dig < 6 : # numeros enter 0 y 6
                if l == 10:                   
                    return __validar_ced_ruc(nro,0)                       
                elif l == 13:
                    return __validar_ced_ruc(nro,0) and nro[10:13] != '000' # se verifica q los ultimos numeros no sean 000
            elif tercer_dig == 6:
                
                return __validar_ced_ruc(nro,1) # sociedades publicas
            elif tercer_dig == 9: # si es ruc
                return __validar_ced_ruc(nro,2) # sociedades privadas
            else:
                return 'Tercer digito invalido'
        else:
            return 'Codigo de provincia incorrecto'
    else:
        return 'Longitud incorrecta del numero ingresado'


def __validar_ced_ruc(nro,tipo):
    total = 0
    if tipo == 0: # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])# digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1: # r.u.c. publicos
        return 'La cedula debe contener 10 digitos'
    elif tipo == 2: # r.u.c. juridicos y extranjeros sin cedula
        return 'La cedula debe contener 10 digitos'
    for i in range(0,len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total+=p if p < 10 else int(str(p)[0])+int(str(p)[1])
        else:
            total+=p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver



@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })


@login_required
def usuarios(request):
    usuarios_list = CustomUser.objects.all()

    if request.method == "POST":
        export = []
        # Se agregan los encabezados de las columnas
        export.append([
            'Nombre',
            'Cedula',
            'Contacto',
            'Correo',
            'Usuario',
            "Estado", ])

        # Se obtienen los datos de la tabla o model y se agregan al array

        for result in usuarios_list:
            # ejemplo para dar formato a fechas, estados (si/no, ok/fail) o
            # acceder a campos con relaciones y no solo al id
            export.append([

                result.first_name,
                result.cedula,
                result.celular,
                result.email,
                result.username,
                result.estado,
            ])

        #sheet = excel.pe.Sheet(export)
        
        #return excel.make_response(sheet, "xlsx", file_name="usuarios.xlsx")
        return ExcelResponse(export, 'usuarios/inicio.html')

    if request.method == "GET":
        search_text = request.GET.get("search", None)
        if search_text is not None:
            records = CustomUser.objects.filter(cedula__contains=search_text)
            return render(request, 'usuarios/inicio.html', {"usuarios": records, "mensaje": "Se encontro {}, usuarios".format(records.count())})
        else:
            return render(request, 'usuarios/inicio.html', {"usuarios": usuarios_list})


@login_required
def new_usuarios(request):
    if request.method == "POST":
        result=verificar_cedula(request.POST.get("cedula",""))
        if result == True:
            form = RegisterUserForms(request.POST)
            if form.is_valid():
                user = CustomUser()
                user.username = form.cleaned_data['username']
                user.set_password(form.cleaned_data['password'])
                user.first_name = form.cleaned_data['first_name']
                user.cedula = form.cleaned_data['cedula']
                user.email = form.cleaned_data['email']
                user.celular = form.cleaned_data['celular']
                user.estado = True
                user.save()
                messages.success(request, "Usuario registrado con éxito !")
                return redirect("usuarios")
            else:
                return render(request, 'usuarios/nuevo.html', {"form": form})
        else:
            return render(request, 'usuarios/nuevo.html', {"error": "Cedula incorrecta"})

    return render(request, 'usuarios/nuevo.html')


@login_required
def actualizar_usuario(request, id):
    usuario_update = CustomUser.objects.get(pk=id)
    if request.method == "POST":
        form = UpdateUserForms(request.POST, instance=usuario_update)
        if form.is_valid():
            usuario_update.username = form.cleaned_data['username']
            usuario_update.first_name = form.cleaned_data['first_name']
            usuario_update.cedula = form.cleaned_data['cedula']
            usuario_update.email = form.cleaned_data['email']
            usuario_update.celular = form.cleaned_data['celular']
            usuario_update.save()
            messages.success(request, "Usuario actualizado con éxito !")

            return redirect("usuarios")
        else:
            return render(request, 'usuarios/edit.html', {"form": form})

    return render(request, 'usuarios/edit.html', {"usuario": usuario_update})


@login_required
def delete_usuario(request, id):

    usuarios_delete = CustomUser.objects.get(pk=id)
    usuarios_delete.estado=False
    usuarios_delete.save()
    messages.success(request, "Usuario eliminado con éxito !")

    return redirect("usuarios")

@login_required
def activar_usuario(request, id):
    usuario_delete = CustomUser.objects.get(pk=id)
    usuario_delete.estado=True
    usuario_delete.save()
    messages.success(request, "Usuario activado con éxito !")

    return redirect("usuarios")


@login_required
def plantas(request):
    plantas_list = Planta.objects.all()
    if request.method == "POST":
        export = []
        # Se agregan los encabezados de las columnas
        export.append([
            'Nombre de la planta',
            'Nombre cientifico',
            'Familia',
            'Genero',

        ])

        # Se obtienen los datos de la tabla o model y se agregan al array

        for result in plantas_list:
            # ejemplo para dar formato a fechas, estados (si/no, ok/fail) o
            # acceder a campos con relaciones y no solo al id
            export.append([

                result.nombre_planta,
                result.nombre_cientifico,
                result.familia,
                result.genero,


            ])

        #sheet = excel.pe.Sheet(export)
        #return excel.make_response(sheet, "xlsx", file_name="plantas.xlsx")
        return ExcelResponse(export, 'plantas/inicio.html')
    if request.method == "GET":
        search_text = request.GET.get("search", None)
        if search_text is not None:
            records = Planta.objects.filter(
                nombre_planta__contains=search_text)
            return render(request, 'plantas/inicio.html', {"plantas": records, "mensaje": "Se encontro {}, plantas".format(records.count())})
        else:
            return render(request, 'plantas/inicio.html', {"plantas": plantas_list})


@login_required
def new_planta(request):
    if request.method == "POST":
        form = RegisterPantaForms(request.POST, request.FILES)
        imagen = request.POST.get("imagen", None)
        print(imagen)
        if form.is_valid():
            form.save()
            messages.success(request, "Planta registrada con éxito !")

            return redirect("plantas")
        else:
            return render(request, 'plantas/nuevo.html', {"form": form})

    return render(request, 'plantas/nuevo.html')


@login_required
def actualizar_planta(request, id):

    planta_update = Planta.objects.get(pk=id)

    if request.method == "POST":
        form = RegisterPantaForms(
            request.POST, files=request.FILES, instance=planta_update)
        if form.is_valid():
            form.save()
            messages.success(request, "Planta actualizada con éxito !")

            return redirect("plantas")
        else:
            print(form)
            return render(request, 'plantas/edit.html', {"form": form})

    return render(request, 'plantas/edit.html', {"planta": planta_update})


@login_required
def delete_planta(request, id):

    planta_delete = Planta.objects.get(pk=id)

    planta_delete.delete()
    messages.success(request, "Planta eliminada con éxito !")

    return redirect("plantas")


@login_required
def fincas(request):
    fincas_list = Finca.objects.all()
    if request.method == "POST":
        export = []
        # Se agregan los encabezados de las columnas
        export.append([
            'Nombre de la finca',
            'Ubicacipon',
            'Latitud',
            'Longitud',
            'Propietario',

        ])

        # Se obtienen los datos de la tabla o model y se agregan al array

        for result in fincas_list:
            # ejemplo para dar formato a fechas, estados (si/no, ok/fail) o
            # acceder a campos con relaciones y no solo al id
            export.append([

                result.nombre_finca,
                result.ubicacion,
                result.latitud,
                result.longitud,
                result.propietario.first_name

            ])

        #sheet = excel.pe.Sheet(export)
        #return excel.make_response(sheet, "xlsx", file_name="fincas.xlsx")
        return ExcelResponse(export, 'fincas/inicio.html')
    if request.method == "GET":
        search_text = request.GET.get("search", None)
        if search_text is not None:
            records = Finca.objects.filter(nombre_finca__contains=search_text)
            return render(request, 'fincas/inicio.html', {"fincas": records, "mensaje": "Se encontro {}, fincas".format(records.count())})
        else:
            return render(request, 'fincas/inicio.html', {"fincas": fincas_list})


@login_required
def new_finca(request):
    propietarios = CustomUser.objects.filter(is_staff=False)
    if request.method == "POST":
        form = RegisterFincasForms(request.POST, files=request.FILES,)
        if form.is_valid():
            form.save()
            messages.success(request, "Finca registrada con éxito !")

            return redirect("fincas")
        else:
            return render(request, 'fincas/nuevo.html', {"form": form, "propietarios": propietarios})

    return render(request, 'fincas/nuevo.html', {"propietarios": propietarios})


@login_required
def perfil_fincas(request,id):
    if request.user.is_staff:
        finca = Finca.objects.get(id=id)
        cultivos_finca=Cultivo.objects.filter(finca=id).order_by('nombre_lote')
        expedientes_finca=Expediente.objects.filter(finca=id)
        return render(request, 'fincas/perfil_finca.html',{"finca":finca,"cultivos":cultivos_finca,"expedientes":expedientes_finca} )
    else:
        propietario= CustomUser.objects.get(id=id)
        print(propietario)
        if propietario is not None:
            try:
                finca = Finca.objects.get(propietario=propietario.pk)
                cultivos_finca=Cultivo.objects.filter(finca=finca.pk)
                expedientes_finca=Expediente.objects.filter(finca=finca.pk)
                return render(request, 'fincas/perfil_finca.html',{"finca":finca,"cultivos":cultivos_finca,"expedientes":expedientes_finca,} )
            except Finca.DoesNotExist:
                return render(request, 'fincas/perfil_finca.html',{"finca":{},"cultivos":{},"expedientes":{}} )
                pass
        else:
            return render(request, 'fincas/perfil_finca.html',{"finca":{},"cultivos":{},"expedientes":{}} )


@login_required
def actualizar_finca(request, id):
    finca_update = Finca.objects.get(pk=id)

    propietarios = CustomUser.objects.filter(is_staff=False)
    if request.method == "POST":
        form = RegisterFincasForms(
            request.POST, files=request.FILES, instance=finca_update)
        if form.is_valid():
            form.save()
            messages.success(request, "Finca actualizada con éxito !")

            return redirect("fincas")
        else:
            return render(request, 'fincas/edit.html', {"form": form, "propietarios": propietarios, "finca": finca_update})

    return render(request, 'fincas/edit.html', {"propietarios": propietarios, "finca": finca_update})


@login_required
def delete_finca(request, id):
    finca_delete = Finca.objects.get(pk=id)

    finca_delete.estado=False
    finca_delete.save()
    messages.success(request, "Finca eliminada con éxito !")

    return redirect("fincas")

@login_required
def activar_finca(request, id):
    finca_delete = Finca.objects.get(pk=id)

    finca_delete.estado=True
    finca_delete.save()
    messages.success(request, "Finca activada con éxito !")

    return redirect("fincas")


@login_required
def cultivos(request):
    cultivo_list = Cultivo.objects.all()

    if request.method == "POST":
        export = []
        # Se agregan los encabezados de las columnas
        export.append([
            'Nombre del lote',
            'Dimensión',
            'Fecha Siembra',
            'Tiempo de cosecha',
            'Planta',
            'Finca',

        ])

        # Se obtienen los datos de la tabla o model y se agregan al array

        for result in cultivo_list:
            # ejemplo para dar formato a fechas, estados (si/no, ok/fail) o
            # acceder a campos con relaciones y no solo al id
            export.append([

                result.nombre_lote,
                result.dimancion_lote,
                result.fecha_siembra,
                result.tiempo_cosecha,
                result.planta.nombre_planta,
                result.finca.nombre_finca

            ])

        #sheet = excel.pe.Sheet(export)
        #return excel.make_response(sheet, "xlsx", file_name="cultivos.xlsx")
        return ExcelResponse(export, 'cultivos/inicio.html')
    if request.method == "GET":
        search_text = request.GET.get("search", None)
        if search_text is not None:
            records = Cultivo.objects.filter(
                finca__nombre_finca__contains=search_text)
            return render(request, 'cultivos/inicio.html', {"cultivos": records, "mensaje": "Se encontro {}, cultivos".format(records.count())})
        else:
            return render(request, 'cultivos/inicio.html', {"cultivos": cultivo_list})


@login_required
def new_cultivo(request):
    plantas = Planta.objects.all()
    fincas = Finca.objects.all()
    if request.method == "POST":
        form = RegisterCultivoForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cultivo registrado con éxito !")

            return redirect("cultivos")
        else:
            return render(request, 'cultivos/nuevo.html', {"form": form, "plantas": plantas, "fincas": fincas})

    return render(request, 'cultivos/nuevo.html', {"plantas": plantas, "fincas": fincas})


@login_required
def actualizar_cultivo(request, id):
    cultivo_update = Cultivo.objects.get(pk=id)
    fecha = cultivo_update.fecha_siembra.strftime('%d/%m/%Y')
    cultivo_update.fecha_siembra.strftime('%d/%m/%Y')

    plantas = Planta.objects.all()
    fincas = Finca.objects.all()
    if request.method == "POST":
        form = RegisterCultivoForms(request.POST, instance=cultivo_update)
        if form.is_valid():
            form.save()
            messages.success(request, "Cultivo actualizado con éxito !")

            return redirect("cultivos")
        else:
            print(form)
            return render(request, 'cultivos/edit.html', {"form": form, "plantas": plantas, "fincas": fincas})

    return render(request, 'cultivos/edit.html', {"plantas": plantas, "cultivo": cultivo_update, "fecha": fecha, "fincas": fincas})


@login_required
def delete_cultivo(request, id):
    cultivo_delete = Cultivo.objects.get(pk=id)

    cultivo_delete.delete()
    messages.success(request, "Cultivo eliminado con éxito !")

    return redirect("cultivos")

import json
from django.core import serializers
def retonarCultivos(request):
    cultivos=Cultivo.objects.all()
    lista=[]
    for cultivo in cultivos:      
        lista.append({
            "planta":cultivo.planta.nombre_planta,
            "finca":cultivo.finca.nombre_finca,            
        })
    return response.JsonResponse({"cultivos":lista})

@ login_required
def estadistica_cultivo(request):
    list_cultivos = Cultivo.objects.all()
    list_fincas = Finca.objects.all()
    list_plantas = Planta.objects.all()
    voto = []
    planta = []
    f = 0
    p = 0
    for cultivo in list_cultivos:
        for finca in list_fincas:
            for plantita in list_plantas:
               
                planta.append(plantita.nombre_planta)
                voto.append(p)
    nombreplanta = simplejson.dumps(planta)
    voto = simplejson.dumps(voto)
    context={
        'nombreplanta':nombreplanta,
        'voto':voto,
        'f':f,
    }
    print(nombreplanta)
    return render(request,'cultivos/estadistica.html', context)

 


@login_required
def expedientes(request):
    expedientes_list = Expediente.objects.all()
    if request.method == "POST":
        export = []
        export.append([
            'Finca',
            'Propietario',
            'Dirección',
            'Total cultivos',
            'Identificacion',
            'Plantas existentes',
            'Total plantas',

        ])
        for result in expedientes_list:
            export.append([
                result.finca.nombre_finca,
                result.propietario.first_name,
                result.direccion,
                result.total_cultivos,
                result.identificacion,
                result.plantas_existentes,
                result.total_plantas,
                 ])

        #sheet = excel.pe.Sheet(export)
        #return excel.make_response(sheet, "xlsx", file_name="expdientes.xlsx")
        return ExcelResponse(export, 'expedientes/inicio.html')
    if request.method == "GET":
        search_text = request.GET.get("search", None)
        if search_text is not None:
            records = Planta.objects.filter(
                nombre_planta__contains=search_text)
            return render(request, 'expedientes/inicio.html', {"expedientes": records, "mensaje": "Se encontro {}, expedientes".format(records.count())})
        else:
            return render(request, 'expedientes/inicio.html', {"expedientes": expedientes_list})


@login_required
def new_expediente(request):
    fincas_list = Finca.objects.all()
    propietarios_list = CustomUser.objects.filter(is_staff=False)
    cultivos_list = Cultivo.objects.all()
    if request.method == "GET":
        print("jkasdbjk")
        pass
    if request.method == "POST":
        form = RegisterExpedientesForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expediente creado con éxito !")

            return redirect("expedientes")
        else:

            return render(request, 'expedientes/nuevo.html', {"form": form, "cultivos": cultivos_list, "fincas": fincas_list, "propietarios": propietarios_list})

    return render(request, 'expedientes/nuevo.html', {"expedientes": cultivos_list, "fincas": fincas_list, "propietarios": propietarios_list})


@login_required
def actualizar_expediente(request, id):
    expediente_update = Expediente.objects.get(pk=id)

    fincas_list = Finca.objects.all()
    propietarios_list = CustomUser.objects.filter(is_staff=False)
    cultivos_list = Cultivo.objects.all()
    if request.method == "POST":
        form = RegisterExpedientesForms(
            request.POST, instance=expediente_update)
        if form.is_valid():
            form.save()
            messages.success(request, "Expediente creado con éxito !")

            return redirect("expedientes")
        else:
            print(form)
            return render(request, 'expedientes/edit.html', {"form": form, "cultivos": cultivos_list, "fincas": fincas_list, "propietarios": propietarios_list})

    return render(request, 'expedientes/edit.html', {"expediente": expediente_update, "cultivos": cultivos_list, "fincas": fincas_list, "propietarios": propietarios_list})


@login_required
def delete_expediente(request, id):
    cultivo_delete = Expediente.objects.get(pk=id)

    cultivo_delete.delete()
    messages.success(request, "Expediente eliminado con éxito !")

    return redirect("expedientes")


def obtener_datos(request):
    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        finca_name = post_data["finca"]
        finca_select = Finca.objects.filter(nombre_finca=finca_name).values()
        propietario_select = CustomUser.objects.filter(
            pk=finca_select[0]["propietario_id"]).values()
        cultivos = Cultivo.objects.filter(
            finca_id=finca_select[0]["id"]).values()

        plantas = []
        numero_plantas = 0
        for cul in cultivos:
            planta = Planta.objects.get(pk=cul["planta_id"])
            # numero_plantas = numero_plantas+int(cul["planta_id"])  
            plantas.append(planta.nombre_planta)

        return response.JsonResponse({
            "finca": list(finca_select)[0]["id"],
            "direccion": list(finca_select)[0]["ubicacion"],
            "identificacion": "",
            "propietario": list(propietario_select)[0]["id"],
            "total_cultivos": cultivos.count(),
            "plantas_existentes": plantas,
            "total_plantas": numero_plantas
        })



def verificar(nro):
    l = len(nro)
    if l == 10 or l == 13: # verificar la longitud correcta
        cp = int(nro[0:2])
        if cp >= 1 and cp <= 22: # verificar codigo de provincia
            tercer_dig = int(nro[2])
            if tercer_dig >= 0 and tercer_dig < 6 : # numeros enter 0 y 6
                if l == 10:                   
                    return __validar_ced_ruc(nro,0)                       
                elif l == 13:
                    return __validar_ced_ruc(nro,0) and nro[10:13] != '000' # se verifica q los ultimos numeros no sean 000
            elif tercer_dig == 6:
                print("askdndkjksabndkaj")
                return __validar_ced_ruc(nro,1) # sociedades publicas
            elif tercer_dig == 9: # si es ruc
                return __validar_ced_ruc(nro,2) # sociedades privadas
            else:
                raise Exception(u'Tercer digito invalido') 
        else:
            raise Exception(u'Codigo de provincia incorrecto') 
    else:
        raise Exception(u'Longitud incorrecta del numero ingresado')


def __validar_ced_ruc(nro,tipo):
    total = 0
    if tipo == 0: # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])# digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1: # r.u.c. publicos
        raise Exception(u'La cedula debe contener 10 digitos') 
    elif tipo == 2: # r.u.c. juridicos y extranjeros sin cedula
        raise Exception(u'La cedula debe contener 10 digitos') 
    for i in range(0,len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total+=p if p < 10 else int(str(p)[0])+int(str(p)[1])
        else:
            total+=p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver

