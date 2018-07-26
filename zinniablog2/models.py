from __future__ import unicode_literals

from django.db import models
import datetime
import django
from django.template.defaultfilters import slugify

from django.utils import timezone

# Create your models here.



class Categoria(models.Model):
    nombre = models.CharField(max_length=250)
    slug = models.SlugField(max_length=230)

    class Meta:
        ordering = ('nombre',)
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nombre


LAYOUT_CHOICES = (
    ('activo','Activo'),
    ('desactivo','Desactivo'),
)


class Perfil(models.Model):
    fecha_creacion = models.DateTimeField(auto_created=True, editable=False, null=True, blank=True)
    activo = models.BooleanField(default=True)
    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='activo')
    image = models.ImageField(null=True, help_text='Imagen Principal.')
    nombre_Scort = models.CharField(max_length=40, help_text='40 characters max.')
    ciudad_Scort = models.CharField(max_length=40, blank=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT)
    slug = models.SlugField(max_length=222, unique=True)



    def __unicode__(self):
        return u'%s, %s' % (self.nombre_Scort, self.ciudad_Scort)


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.categoria)
        super(Perfil, self).save(*args, **kwargs)
