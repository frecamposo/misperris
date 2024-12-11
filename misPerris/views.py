import re
from django.shortcuts import render
# importamos los modelos de tabla de la BDD
from .models import Categoria, Mascota, Galeria

# importar el modelo de tabla User 
from django.contrib.auth.models import User
# importar librerias que permitan la validacion del login
from django.contrib.auth import authenticate,logout,login as login_aut
# importar libreria decoradora que permite evitar el ingreso de usuarios a las paginas web
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def crear_usuario(request):
    if request.POST:
        nombre = request.POST.get("txtNombre")
        apellido = request.POST.get("txtApellido")
        nom_usuario = request.POST.get("txtUsuario")
        email = request.POST.get("txtEmail")
        pass1 = request.POST.get("txtPass1")
        pass2 = request.POST.get("txtPass2")

        if pass1!=pass2:
            contexto= {"mensaje":"contraseñas son diferentes"}
            return render(request,"crear_usuario.html",contexto)

        try:
            usu = User.objects.get(username=nom_usuario)
            contexto = {"mensaje":"nombre de usuario existe"}
            return render(request,"crear_usuario.html",contexto)
        except:    
            usu = User()
            usu.first_name=nombre
            usu.last_name=apellido
            usu.email=email
            usu.username=nom_usuario
            usu.set_password(pass1)
            usu.save()

            us = authenticate(request,username=nom_usuario,password=pass1)
            login_aut(request,us)

            categorias = Categoria.objects.all()
            contex = {"categorias":categorias}
            return render(request, "index.html",contex)        
    return render(request,"crear_usuario.html")

def cerrar_sesion(request):
    categorias = Categoria.objects.all()
    contex = {"categorias":categorias}
    logout(request)
    return render(request,"index.html",contex)

def login(request):
    categorias = Categoria.objects.all()
    contexto = {"categorias":categorias}
    if request.POST:
        nombre = request.POST.get("txtUsuario")
        password = request.POST.get("txtPass")
        us = authenticate(request,username=nombre,password=password)
        if us is not None and us.is_active:
            login_aut(request,us)
            return render(request,"index.html",contexto)
        else:
            contexto = {"mensaje":"usuario y contraseña incorrecto","categorias":categorias}
            return render(request,"login.html",contexto)        
    return render(request,"login.html")

def index(request):
    categorias = Categoria.objects.all()
    mascotas = Mascota.objects.filter(publicar=True).order_by('-nombre')[:3]
    contex = {"categorias":categorias,"mascotas":mascotas}
    return render(request, "index.html",contex)

def galeria(request):
    mascotas = Mascota.objects.filter(publicar=True)
    categorias = Categoria.objects.all()
    contexto = {"mascotas":mascotas,"categorias":categorias}
    return render(request, "galeria.html",contexto)

def filtro_cate(request, id):
    categorias = Categoria.objects.all()
    obj_cate = Categoria.objects.get(nombre=id)
    mascotas = Mascota.objects.filter(categoria=obj_cate).filter(publicar=True)
    cant = Mascota.objects.filter(categoria=obj_cate).filter(publicar=True).count()
    contexto = {"mascotas":mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria.html",contexto)   

def filtro_categoria(request):
    mascotas = Mascota.objects.filter(publicar=True)
    categorias = Categoria.objects.all()
    cant = Mascota.objects.filter(publicar=True).count()
    if request.POST:
        categoria = request.POST.get("cboCategoria")
        obj_cate = Categoria.objects.get(nombre=categoria)
        mascotas = Mascota.objects.filter(categoria=obj_cate).filter(publicar=True)
        cant = Mascota.objects.filter(categoria=obj_cate).filter(publicar=True).count()
    contexto = {"mascotas":mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria.html",contexto)   

def buscar_nombre_mascota(request):
    mascotas = Mascota.objects.filter(publicar=True)
    categorias = Categoria.objects.all()
    if request.POST:
        nombre = request.POST.get("txtNombre")
        mascotas = Mascota.objects.filter(nombre=nombre).filter(publicar=True)
    contexto = {"mascotas":mascotas,"categorias":categorias}
    return render(request, "galeria.html",contexto)   

def filtro_desc(request):
    mascotas = Mascota.objects.filter(publicar=True)
    categorias = Categoria.objects.all()
    if request.POST:
        desc = request.POST.get("txtDesc")
        mascotas = Mascota.objects.filter(descripcion__contains=desc).filter(publicar=True)
    contexto = {"mascotas":mascotas,"categorias":categorias}
    return render(request, "galeria.html",contexto)   

def formulario(request):
    return render(request, "formulario.html")

def ficha_mascota(request, id):
    mascota = Mascota.objects.get(nombre=id) # select * from Mascota where nombre=id
    galeria = Galeria.objects.filter(mascota= mascota)
    contexto = {"mascota":mascota, "galeria":galeria}
    return render(request,"ficha.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.add_mascota',login_url='/login/')
def registro(request):
    nom_user = request.user.username # recupero del request el usuario (login)
    registros = Categoria.objects.all() # select * from Categoria
    mensaje=""
    if request.POST:
        nombre = request.POST.get("txtNombre")
        edad = request.POST.get("txtEdad")
        desc = request.POST.get("txtDesc")
        cate = request.POST.get("cboCategoria")
        ima  = request.FILES.get("txtImg")
        # select * from Categoria where nombre='Perros' --> recupera el registro
        obj_cate = Categoria.objects.get(nombre=cate)
        try:
            mas = Mascota.objects.get(nombre=nombre)
            mensaje="Mascota Existe"
        except:
            mas = Mascota()
            mas.nombre=nombre
            mas.edad=edad
            mas.descripcion=desc
            if ima is not None:
                mas.imagen= ima
            mas.categoria=obj_cate
            mas.usuario = nom_user
            mensaje="Mascota Almacaneda"
            mas.save()

    mascotas= Mascota.objects.filter(usuario=nom_user)
    contexto = {"categorias":registros, "mensaje":mensaje,"mascotas":mascotas}
    return render(request, "registro.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.delete_mascota',login_url='/login/')
def eliminar_mascota(request, id):
    mas = Mascota.objects.get(nombre=id)
    mas.delete()
    mensaje = "mascota eliminada"
    registros = Categoria.objects.all()
    mascotas= Mascota.objects.all()
    contexto = {"categorias":registros, "mensaje":mensaje,"mascotas":mascotas}
    return render(request, "registro.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.change_mascota',login_url='/login/')
def modificar_mascota(request, id):
    mas = Mascota.objects.get(nombre=id)    
    registros = Categoria.objects.all()   
    contexto = {"categorias":registros,"mascota":mas}
    return render(request, "modificar.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.change_mascota',login_url='/login/')
def modificacion(request):
    mensaje=""
    nom_user = request.user.username
    if request.POST:
        nombre = request.POST.get("txtNombre")
        edad = request.POST.get("txtEdad")
        desc = request.POST.get("txtDesc")
        cate = request.POST.get("cboCategoria")
        ima  = request.FILES.get("txtImg")
        # select * from Categoria where nombre='Perros' --> recupera el registro
        obj_cate = Categoria.objects.get(nombre=cate) 

        try:
            mas = Mascota.objects.get(nombre=nombre)
            mas.edad= edad
            mas.descripcion = desc
            mas.categoria = obj_cate

            if ima is not None:
                mas.imagen = ima
            
            mas.comentario='--'        
            mas.save()
            mensaje="modifico mascota "+nombre
        except:
            mensaje="no modifico mascota "+nombre
            
    registros = Categoria.objects.all()
    mascotas= Mascota.objects.filter(usuario=nom_user)
    contexto = {"categorias":registros, "mensaje":mensaje,"mascotas":mascotas}
    return render(request, "registro.html",contexto)

@login_required(login_url='/login/')
def adoptar(request,id):
    try:
        mas = Mascota.objects.get(nombre=id)
        mas.dueno = request.user.username
        mas.publicar = False
        mas.comentario = 'Adoptado'
        mas.save()
        mensaje="Adoptado"
        contexto = {"mascota":mas,"mensaje":mensaje}
        return render(request,"ficha.html",contexto)
    except:
        mensaje="no pudo adoptarla"
        categorias = Categoria.objects.all()
        contex = {"categorias":categorias,"mensaje":mensaje}
        return render(request, "index.html",contex)

def admin_usuario(request):
    mascotas = Mascota.objects.filter(dueno=request.user.username)
    contexto = {"mascotas":mascotas}
    return render(request,"admin_usuario.html",contexto)

def devolver(request,id):
    mensaje=''
    try:
        mas = Mascota.objects.filter(publicar=False).get(nombre=id)
        mas.dueno='--'
        mas.comentario='--'
        mas.save()
        mensaje='Mascota ' +id+' Devuelta'
    except:
        mensaje='Mascota No Devuelta'
    
    mascotas = Mascota.objects.filter(dueno=request.user.username)
    contexto = {"mascotas":mascotas,"mensaje":mensaje}
    return render(request,"admin_usuario.html",contexto)
  
def insertar_galeria(request):
    mensaje=""
    if request.POST:
        nom_mascota = request.POST.get("txtMascota")
        imagen = request.FILES.get("txtImg")
        obj_mascota = Mascota.objects.get(nombre=nom_mascota)

        gale = Galeria()
        gale.imagen = imagen
        gale.mascota = obj_mascota
        gale.save()
        mensaje = "Agrego Imagen para mascota "+nom_mascota

    nom_user = request.user.username
    mascotas= Mascota.objects.filter(usuario=nom_user)
    registros = Categoria.objects.all()
    contexto = {"categorias":registros, "mensaje":mensaje,"mascotas":mascotas}
    return render(request, "registro.html",contexto)

