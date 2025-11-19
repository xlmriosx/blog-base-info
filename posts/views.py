from django.shortcuts import render
from .models import Post, Categoria

# Create your views here.
def listar(request):
    context = {}

    id_categoria = request.GET.get('id', None)

    if id_categoria:
        n = Post.objects.filter(categoria_post = id_categoria)
    else:
        n = Post.objects.all()

    context['posts'] = n

    cat = Categoria.objects.all().order_by('nombre')
    context['categoria'] = cat

    return render(request, 'posts/listar.html', context)