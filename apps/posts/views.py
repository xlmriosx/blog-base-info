from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Categoria, Comentario, PostImage
from .forms import PostForm, ComentarioForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse

def is_collaborator(user):
    return user.is_authenticated and user.es_colaborador

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

    n = get_object_or_404(Post, pk=pk)
    context['post'] = n

    c = Comentario.objects.filter(post = n).order_by('-fecha_publicacion')
    context['comentarios'] = c
    context['form'] = ComentarioForm() # For the comment form in detail view

    return render(request, 'posts/detalle.html', context)

@login_required
def comentar(request):
    if request.method == 'POST':
        # Manually create the form with the 'comentario' field from the template
        # The template sends 'comentario' but the form expects 'texto'
        texto = request.POST.get('comentario')
        id_post = request.POST.get('id_post', None)

        if texto and id_post:
            post = get_object_or_404(Post, pk=id_post)
            Comentario.objects.create(usuario=request.user, post=post, texto=texto)
            return redirect(reverse_lazy('posts:detalle', kwargs={'pk': id_post}))
    return redirect('posts:listar')

class CollaboratorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.es_colaborador

class PostCreateView(CollaboratorRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:listar')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Handle multiple images
        images = self.request.FILES.getlist('imagenes')
        for image in images:
            PostImage.objects.create(post=self.object, imagen=image)
        return response

class PostUpdateView(CollaboratorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def get_success_url(self):
        return reverse_lazy('posts:detalle', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        # Handle new multiple images
        images = self.request.FILES.getlist('imagenes')
        for image in images:
            PostImage.objects.create(post=self.object, imagen=image)
        return response

class PostDeleteView(CollaboratorRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:listar')

class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'posts/comentario_form.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.es_colaborador:
            return qs
        return qs.filter(usuario=self.request.user)

    def get_success_url(self):
        return reverse_lazy('posts:detalle', kwargs={'pk': self.object.post.pk})

class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'posts/comentario_confirm_delete.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.es_colaborador:
            return qs
        return qs.filter(usuario=self.request.user)

    def get_success_url(self):
        return reverse_lazy('posts:detalle', kwargs={'pk': self.object.post.pk})
