# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.views.generic import ListView, DetailView
from .models import Perfil
from django.shortcuts import render, redirect

from contacto.forms import ContactoForm
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

# Create your views here.


class IndexView(ListView):

    template_name = 'index.html'
    model = Perfil

class PerfilDetailView(DetailView):

    template_name = 'entrada_detail.html'
    model = Perfil

