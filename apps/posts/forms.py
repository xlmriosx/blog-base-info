from django import forms
from .models import Post, PostImage, Comentario

class PostForm(forms.ModelForm):
    imagenes = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False, label="Imágenes adicionales")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagenes'].widget.attrs.update({'multiple': True})

    class Meta:
        model = Post
        fields = ['titulo', 'cuerpo', 'categoria_post', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'cuerpo': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria_post': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
