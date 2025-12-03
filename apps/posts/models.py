from django.db import models

from apps.usuarios.models import Usuario

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Post(models.Model):
    titulo = models.CharField(max_length=150)
    cuerpo = models.TextField()
    categoria_post = models.ForeignKey(Categoria, on_delete= models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='post', null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} {self.fecha}"

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='post_images')

    def __str__(self):
        return f"Imagen de {self.post.titulo}"

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    texto = models.TextField(max_length=1500)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post} -> {self.texto}"