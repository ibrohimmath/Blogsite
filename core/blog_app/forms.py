from django import forms 

from django.contrib.auth import get_user_model 

from blog_app.models import Article, Comment

class UserRegisterForm(forms.Form):
    username = forms.CharField(label = 'Username', widget = forms.TextInput(attrs = {'placeholder': 'usernameni kiriting'}))
    email = forms.EmailField(label = 'Email', widget = forms.TextInput(attrs = {'placeholder': 'e-mail adresni kiriting'}))
    password1 = forms.CharField(label = 'Parol', widget = forms.TextInput(attrs = {'type': 'password', 'placeholder': 'parolni kiriting'}))    
    password2 = forms.CharField(label = 'Parolni takrorlang', widget = forms.TextInput(attrs = {'type': 'password'}))
    
class UserLoginForm(forms.Form):
    username = forms.CharField(label = 'Username', widget = forms.TextInput(attrs = {'placeholder': 'usernameni kiriting'}))
    password = forms.CharField(label = 'Parol', widget = forms.TextInput(attrs = {'type': 'password', 'placeholder': 'parolni kiriting'}))    
    
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article 
        fields = ['title', 'description', 'image', 'tags']

        
    