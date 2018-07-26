from django import forms

from .models import Contacto


class ContactoForm(forms.ModelForm):


    nombre = forms.CharField(label='nombre',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

    apellido = forms.CharField(label='apellido',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

    celular = forms.CharField(label='celular', widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class':'form-control'}
    ))

    mensaje = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '5', 'rows': '10', 'class': 'form-control'}
    ))

    class Meta:
        model = Contacto
        fields = ('nombre', 'apellido', 'email', 'celular','mensaje')

