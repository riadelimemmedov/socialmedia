from django import forms
from .models import *

class UpdateAccount(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['created','user']

class ContactForm(forms.ModelForm):#Burda modelForm yazilmasindaki sebeb her hansi bir modelden miras alib istifade edirik ona gore forms.ModelForm dan istifade ettik eger sifirdan bir form yaratmag isteyirnses onda forms.Form dan istifad et
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'id':'contact-name',
        'placeholder':'Adinizi Girin',
        'class':'form-control requiredField Highlighted-label',
        'type':'text'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={#formda istifade olunan widget ve attrs ile css classlarini burda istifade edib sonra html seyfesine gondermek mumkundur
        'id':'contact-mail',
        'placeholder':'Email Girin',
        'class':'form-control requiredField Highlighted-label',
        'type':'email',
    }))
    
    message = forms.CharField(widget=forms.Textarea(attrs={
        'id':'contact-message',
        'placeholder':'Mesaj Girin',
        'class':'form-control requiredField Highlighted-label',
        'rows':6
    }))
    
    class Meta:
        model = Contact
        fields = ['name','email','message']