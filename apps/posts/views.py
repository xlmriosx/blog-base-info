from django.shortcuts import render, redirect
from .models import Post, Categoria, Comentario

from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy

# Create your views here.
def listar(request):
    context = {}

    id_categoria = request.GET.get('id', None)

    if id_categoria:
        n = Post.objects.filter(categoria_post = id_categoria)
    else:
        n = Post.objects.all().order_by('-fecha')

    context['posts'] = n

    cat = Categoria.objects.all().order_by('nombre')
    context['categoria'] = cat

    return render(request, 'posts/listar.html', context)

def detalle(request, pk):
    context = {}

    n = Post.objects.get(pk = pk)
    context['post'] = n

    c = Comentario.objects.filter(post = n).order_by('-fecha_publicacion')
    context['comentarios'] = c

    return render(request, 'posts/detalle.html', context)

@login_required
def comentar(request):
    comentario_content = request.POST.get('comentario', None)
    user = request.user
    id_post = request.POST.get('id_post', None)
    noti = Post.objects.get(pk = id_post)
    Comentario.objects.create(usuario=user, post=noti, texto=comentario_content)

    return redirect(reverse_lazy('posts:detalle', kwargs={'pk': id_post}))
