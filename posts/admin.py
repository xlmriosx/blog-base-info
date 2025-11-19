from django.contrib import admin

# Register your models here.
from .models import Categoria, Post

admin.site.register(Categoria)
admin.site.register(Post)
