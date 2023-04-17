from django.urls import path
from .views import *

urlpatterns = [
    path("", inicio, name="inicio_chat"),
    path("escribir/", escribir_mensaje, name="escribir_mensaje"),
    path("leer/", leer_mensajes, name="ver_mensajes"),
]