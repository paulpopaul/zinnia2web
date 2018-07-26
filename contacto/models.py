# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class Contacto(models.Model):
    fecha = models.DateTimeField(_('fecha'), auto_now=True, blank=True, null=True, )
    nombre = models.CharField('Nombre', max_length=50)
    apellido = models.CharField('Apellido', max_length=50)
    celular = models.CharField('Teléfono', max_length=13)
    email = models.EmailField('Email')
    mensaje = models.TextField()
    history = HistoricalRecords()

    def __unicode__(self):
        return u"%s" % self.nombre

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"
        ordering = ['fecha']

class Detalles(models.Model):
    nombreadmin = models.CharField('Nombre a Mostrar', max_length=50)
    telefonoadmin = models.CharField('Telefono a Mostrar',  max_length=50, help_text="ej: 99887766")

    def __unicode__(self):
        return u"%s" % self.nombreadmin

    class Meta:
        verbose_name = "Mis Datos"
        verbose_name_plural = "Mis Datos"
        ordering = ['nombreadmin']