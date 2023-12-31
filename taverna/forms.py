from django.forms import ModelForm
from .models import Post
from django import forms
from .models import Author

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'title', 'text', 'category']
        widgets = {
            'image' : forms.FileInput(attrs={
                  'class' : 'form-control',
                  'placeholder' : 'Вставте картинку',
                  'id' : 'postform-image-field'
                }),
            'title' : forms.TextInput(attrs={
                  'class' : 'form-control',
                  'placeholder' : 'Заголовок...',
                  'id' : 'postform-title-field'
                }),
            'text' : forms.Textarea(attrs={
                  'class' : 'form-control',
                  'id' : 'postform-text-field'
                }),
            'category' : forms.SelectMultiple(attrs={
                  'class' : 'form-control', 
                  'id' : 'postform-category-field'
                }),
        }

