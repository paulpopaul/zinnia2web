from __future__ import unicode_literals
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from contacto.forms import ContactoForm
from django.core.mail import EmailMultiAlternatives
from zinniablog2.models import Perfil

# Create your views here.

class IndexView(ListView):

    template_name = 'index.html'
    model = Perfil

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['perfil_list'] = Perfil.objects.all().first()
        return context

class PerfilDetailView(DetailView):
    template_name = 'entrada_detail.html'
    model = Perfil

def contacto(request):
    if request.method == "POST":
        contact = ContactoForm(request.POST)
        mensaje_enviado = '/enviando/'
        if contact.is_valid():
            c = contact.save(commit=False)
            c.save()
            to_mail = c.email
            subject, from_email, to = 'Copia Mensaje divinasur', 'scort@divinasur.cl', to_mail,
            text_content = 'Gracias por inscribirte'
            html_content = '<h1>Copia del mensaje en scort@divinasur.cl:</h1><br><p><strong>Mensaje: </strong><br>'+c.mensaje+'</p><br><p><strong>De: </strong>'+c.nombre+'('+c.email+')</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            to_mail = 'scort@divinasur.cl'
            subject, from_email, to = 'Copia Mensaje scort@divinasur.cl', 'scort@divinasur.cl', to_mail,
            text_content = 'Gracias por inscribirte'
            html_content = '<h1>Copia del mensaje en scort@divinasur.cl:</h1><br><p><strong>Mensaje: </strong><br>'+c.mensaje+'</p><br><p><strong>De: </strong>'+c.nombre+'('+c.email+')</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print('Enviado :v')
            return redirect(mensaje_enviado)
    else:
        contact = ContactoForm()
    context = {

        'form': contact,
    }
    return render(request, 'form_contacto.html', context)