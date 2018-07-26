from django.contrib import admin

# Register your models here.
from .models import Contacto, Detalles


class ContactoAdmin(admin.ModelAdmin):
    model = Contacto
    fieldsets = (
        (('Mensaje'), {
            # 'classes': ('collapse',),
            'fields': (('nombre', 'apellido',),('email','celular'),
                       ('mensaje',),
                       ), }),
    )
    list_display = ['nombre', 'apellido', 'fecha']
    search_fields = ('nombre', 'apellido', 'email','celular' , 'mensaje')
    list_filter = ['nombre', 'apellido', 'fecha', ]

admin.site.register(Contacto, ContactoAdmin)

class DetallesAdmin(admin.ModelAdmin):
    model = Detalles
    fieldsets = (
        (('detalles'), {
            # 'classes': ('collapse',),
            'fields': (('nombreadmin', 'telefonoadmin'),) }),
    )
    list_display = ['nombreadmin', 'telefonoadmin',]


admin.site.register(Detalles, DetallesAdmin)