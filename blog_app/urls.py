from django.urls import path
from .views import *


urlpatterns = [
    ########### URLS PRINCIPALES ###########
    path('', inicio, name="inicio"),
    path('sobre_nosotros/', sobre_nosotros, name="sobre_nosotros"),
    path('paginas/', paginas, name="paginas"),
    ########################################

    ########### URLS PUBLICACIONES ##########
    path('paginas/<id_publicacion>', get_pagina, name="get_pagina"),
    path('paginas/crear/', crear_pagina, name="crear_pagina"),
    path('paginas/editar/<id_publicacion>', editar_pagina, name="editar_pagina"),
    path('paginas/eliminar/<id_publicacion>', eliminar_pagina, name="eliminar_pagina"),
    ########################################

    ############# URLS USUARIO #############
    path('perfil/', get_perfil, name="get_perfil"),
    path('perfil/login/', login_request, name="login_request"),
    path('perfil/register/', register, name="register"),
    path('perfil/logout/', Logout.as_view(), name="logout"),
    path('perfil/editar/', editar_perfil, name="editar_perfil"),
    path('perfil/eliminar/', eliminar_perfil, name="eliminar_perfil"),
    ########################################
]