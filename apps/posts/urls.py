from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("", views.listar, name="listar"),
    path("detalle/<int:pk>/", views.detalle, name="detalle"),
    path("comentario/", views.comentar, name="comentar"),

    # Post CRUD
    path("crear/", views.PostCreateView.as_view(), name="post_create"),
    path("editar/<int:pk>/", views.PostUpdateView.as_view(), name="post_update"),
    path("borrar/<int:pk>/", views.PostDeleteView.as_view(), name="post_delete"),

    # Comment CRUD
    path("comentario/editar/<int:pk>/", views.ComentarioUpdateView.as_view(), name="comentario_update"),
    path("comentario/borrar/<int:pk>/", views.ComentarioDeleteView.as_view(), name="comentario_delete"),
]
