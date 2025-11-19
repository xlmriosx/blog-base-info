from django.db import models

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
    imagen = models.ImageField(upload_to='post')

    def __str__(self):
        return f"{self.titulo} {self.fecha}"
