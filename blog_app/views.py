from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import *
from .forms import *


########## VIEWS PRINCIPALES #############

def inicio(request):
    return render(request,"inicio.html")



def sobre_nosotros(request):
    return render(request, "sobre_nosotros.html")



def paginas(request):
    publicaciones = Publicacion.objects.all()
    if not publicaciones.exists():
        return render(request, "leer_paginas.html", {"publicaciones" : publicaciones, "mensaje" : "No hay páginas aún"})
    else:
        return render(request, "leer_paginas.html", {"publicaciones" : publicaciones})

##########################################

######### VIEWS DE PUBLICACIONES #########

def get_pagina(request, id_publicacion):
    publicacion = Publicacion.objects.get(id_publicacion=id_publicacion)
    return render(request, "get_pagina.html", {"publicacion" : publicacion})



@login_required
def crear_pagina(request):
    if request.method == "POST":
        formulario = PublicacionForm(request.POST)
        usuario = request.user.username
        if formulario.is_valid():
            publicacion = Publicacion(
                titulo = request.POST.get("titulo"),
                subtitulo = request.POST.get("subtitulo"),
                contenido = request.POST.get("contenido"),
                autor = usuario
            )
            publicacion.save()

            if 'imagen' in request.FILES:
                img = request.FILES["imagen"]
                imagen = ImagenPublicacion(id_Publicacion=publicacion, imagen=img)
                imagen.save()
            publicaciones = Publicacion.objects.all()
            return render(request, "leer_paginas.html", {"publicaciones" : publicaciones, "mensaje" : "publicación creada correctamente"})
        else:
            return render(request, "crear_pagina.html", {"mensaje" : "Datos inválidos, vuelva a intentarlo", "formulario" : PublicacionForm()})

    else:
        return render(request, "crear_pagina.html", {"formulario" : PublicacionForm()})



@login_required
def editar_pagina(request, id_publicacion):
    publicacion = Publicacion.objects.get(id_publicacion=id_publicacion)
    formulario_viejo = PublicacionForm(initial = {
        "titulo" : publicacion.titulo,
        "subtitulo" : publicacion.subtitulo,
        "contenido" : publicacion.contenido,
    })
    if request.method == "POST":
        formulario_nuevo = PublicacionForm(request.POST)
        if formulario_nuevo.is_valid():
            info = formulario_nuevo.cleaned_data
            publicacion.titulo = info["titulo"]
            publicacion.subtitulo = info["subtitulo"]
            publicacion.contenido = info["contenido"]
            publicacion.save()

            img = ImagenPublicacion.objects.filter(id_Publicacion = publicacion)
            if "imagen" in request.FILES:
                imagen_nueva = request.FILES["imagen"]
                if img.exists():
                    if imagen_nueva:
                        img = img[0]
                        img.imagen = imagen_nueva
                        img.save()
                else:
                    img = ImagenPublicacion(id_Publicacion=publicacion, imagen=imagen_nueva)
                    img.save()

            return render(request, "get_pagina.html", {"mensaje" : "Publicación editada correctamente", "publicacion" : publicacion})
        else:
            return render(request, "editar_pagina.html", {"formulario" : formulario_viejo, "mensaje" : "Datos inválidos, vuelva a intentarlo", "publicacion" : publicacion})

    else:
        return render(request, "editar_pagina.html", {"formulario" : formulario_viejo, "publicacion" : publicacion})



@login_required
def eliminar_pagina(request, id_publicacion):
    publicacion = Publicacion.objects.get(id_publicacion=id_publicacion)
    if request.method == "POST":
        publicacion.delete()
        publicaciones = Publicacion.objects.all()
        return render(request, "leer_paginas.html", {"mensaje" : "Publicacion eliminada correctamente", "publicaciones" : publicaciones})
    else:
        return render(request, "eliminar_paginas.html", {"publicacion" : publicacion})

##########################################

########### VIEWS DEL USUARIO ############

def get_perfil(request):
    usuario = request.user
    return render(request, "get_perfil.html", {"usuario" : usuario})



def login_request(request):
    if request.method == "POST":
        formulario = AuthenticationForm(request, data = request.POST)
        if formulario.is_valid():
            nombre = request.POST["username"]
            contraseña = request.POST["password"]
            user = authenticate(username = nombre, password = contraseña)
            if user is not None:
                login(request, user)
                return render(request, "inicio.html", {"mensaje" : f"Bienvenido {user}"})
            else:
                return render(request, "login.html", {"mensaje" : "Usuario o contraseña incorrectos", "formulario" : AuthenticationForm()})
        else:
            return render(request, "login.html", {"mensaje" : "Usuario o contraseña incorrectos", "formulario" : AuthenticationForm()})

    else:
        formulario = AuthenticationForm()
        return render(request, "login.html", {"formulario" : formulario})



def register(request):
    if request.method == "POST":
        formulario = UserRegisterForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.cleaned_data.get("username")
            formulario.save()
            return render(request, "inicio.html", {"mensaje" : f"Usuario {usuario} creado correctamente"})
        else:
            return render(request, "register.html", {"mensaje" : "Usuario o contraseña incorrectos", "formulario" : formulario})

    else:
        formulario = UserRegisterForm()
        return render(request, "register.html", {"formulario" : formulario})



class Logout(LoginRequiredMixin, LogoutView):
    template_name = "inicio.html"
    extra_context = {"mensaje" : "Te deslogueaste correctamente"}



@login_required
def editar_perfil(request):
    usuario = request.user
    if request.method == "POST":
        formulario_nuevo = UserEditForm(request.POST)
        if formulario_nuevo.is_valid():
            info = formulario_nuevo.cleaned_data
            usuario.email = info["email"]
            usuario.password1 = info["password1"]
            usuario.password2 = info["password2"]
            usuario.first_name = info["first_name"]
            usuario.last_name = info["last_name"]
            usuario.save()
            return render(request, "get_perfil.html", {"usuario" : usuario, "mensaje" : "editado correctamente"})
        else:
            return render(request, "editar_perfil.html", {"formulario" : formulario_nuevo, "mensaje" : "Datos inválidos, vuelva a intentarlo"})

    else:
        formulario_viejo = UserEditForm(instance = usuario)
        return render(request, "editar_perfil.html", {"formulario" : formulario_viejo})



@login_required
def eliminar_perfil(request):
    usuario = request.user
    if request.method == "POST":
        usuario.delete()
        return render(request, "inicio.html", {"mensaje" : "Usuario eliminado correctamente"})
    
    else:
        return render(request, "eliminar_perfil.html", {"usuario" : usuario})

##########################################