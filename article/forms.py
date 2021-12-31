from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from .models import * #yeni model icinde cekirsen hamsini

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':5,'width':50}))
    class Meta:
        model = Post
        fields = ['content','resim','category']
    
class UpdateForm(forms.ModelForm):#burda forms.ModelFormdaki  modelform onu ifade edirki yeni her hansi bir modelden istifade edirik sifirdan bir form yaratmirig
    class Meta:
        model = Post
        fields = ['title', 'content', 'resim','category','tag']
        



class LoginForm(forms.Form):#Burda forms.Form yazilmasindaki sebeb ozumuz sifirdan bir form yaradirig yeni oan gore eger modelden data cekende istifade edeceyikse bu formu onda forms.modelFormdan istifade ederdik
    username = forms.CharField(label='Istifadeci Adi')
    password = forms.CharField(label='Sifre',widget=forms.PasswordInput)



class RegisterForm(UserCreationForm):
    ad = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control form-control-lg',
        'placeholder':'Adiniz'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control form-control-lg',
        'placeholder':'Email'
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control form-control-lg',
        'placeholder':'Sifre'
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control form-control-lg',
        'placeholder':'Sifre Tekrar'
    }))
    
    class Meta:
        model = User
        fields = ['ad','email','password1','password2']
    

class CreatePostForm(forms.ModelForm):#forms.ModelForm burdaki Model Form yeni modelden bir data cekib formda istifade edeciyik
    class Meta:
        model = Post#model=POST bu Class Meta icinde yaz
        fields = ['title','content','resim','category','tag']

class TagForms(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'type':'text',
        'name':'tag',
        'class':'form-control',
        'placeholder':'Tag',
        'aria-label':'Tag',
        'aria-describedby':'basic-addon1'
    }))
    
    # slug = forms.SlugField(widget=forms.TextInput(attrs={
    #     'type':'text',
    #     'name':'slug',
    #     'class':'form-control',
    #     'placeholder':'Slug',
    #     'aria-label':'Slug',
    #     'aria-describedby':'basic-addon1'
    # }))
    class Meta:
        model = Tag
        fields = ['title']