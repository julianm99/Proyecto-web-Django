from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


def inicio(request):
    return render(request, "chat.html")



@login_required
def escribir_mensaje(request):
    usuario = request.user.username
    if request.method == "POST":
        formulario = MensajesForm(request.POST)
        if formulario.is_valid():
            mensaje = Mensajes(
                username = usuario,
                mensaje = request.POST.get('mensaje'),
            )
            mensaje.save()
            return render(request, "escribir_mensaje.html", {"formulario" : MensajesForm(), "mensaje" : "Mensaje guardado exitosamente"})

    else:
        formulario = MensajesForm()
        return render(request, "escribir_mensaje.html", {"formulario" : formulario})



def leer_mensajes(request):
    mensajes = Mensajes.objects.all()
    return render(request, "ver_mensajes.html", {"mensajes" : mensajes})