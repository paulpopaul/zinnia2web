from __future__ import unicode_literals
import datetime
from django.contrib import admin
from .models import Perfil, Categoria


# Register your models here.

admin.site.register(Categoria)
admin.site.register(Perfil)
