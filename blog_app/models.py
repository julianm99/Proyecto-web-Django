from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Publicacion(models.Model):
    id_publicacion= models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=20)
    subtitulo = models.CharField(max_length=20)
    contenido = RichTextUploadingField()
    autor = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Publicacion: {self.titulo} {self.autor}"


class ImagenPublicacion(models.Model):
    id_Publicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='publicacion', null=True, blank=True)
