"""Base entry models for Zinnia"""
import os
import datetime
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

import django_comments as comments
from django_comments.models import CommentFlag

from tagging.fields import TagField
from tagging.utils import parse_tag_input

from zinnia.flags import PINGBACK
from zinnia.flags import TRACKBACK
from zinnia.managers import DRAFT, HIDDEN, PUBLISHED
from zinnia.managers import EntryPublishedManager
from zinnia.managers import entries_published
from zinnia.markups import html_format
from zinnia.preview import HTMLPreview
from zinnia.settings import AUTO_CLOSE_COMMENTS_AFTER
from zinnia.settings import AUTO_CLOSE_PINGBACKS_AFTER
from zinnia.settings import AUTO_CLOSE_TRACKBACKS_AFTER
from zinnia.settings import ENTRY_CONTENT_TEMPLATES
from zinnia.settings import ENTRY_DETAIL_TEMPLATES
from zinnia.settings import UPLOAD_TO
from zinnia.url_shortener import get_url_shortener

from multiselectfield import MultiSelectField





@python_2_unicode_compatible
class CoreEntry(models.Model):
    """
    Abstract core entry model class providing
    the fields and methods required for publishing
    content over time.
    """
    STATUS_CHOICES = ((DRAFT, _('draft')),
                      (HIDDEN, _('hidden')),
                      (PUBLISHED, _('published')))


    title = models.CharField(
        _('Nombre'), max_length=255,
        help_text='Real o fantasía, usado en sitio')

    rut = models.CharField(
        _('Rut'), max_length=13, null=True, blank=True,
        help_text='Solo administración')

    nombreadmin = models.CharField(
        _('Nombre'), max_length=255, null=True, blank=True,
        help_text='Solo administración')

    apellidouno = models.CharField(
        _('Apellido Paterno'), max_length=255, null=True, blank=True,
        help_text='Solo administración')

    apellidodos = models.CharField(
        _('Apellido Materno'), max_length=255, null=True, blank=True,
        help_text='Solo administración')

    concelular = models.CharField(
        _('Teléfono Celular'), max_length=12, null=True, blank=True,
        help_text='ej: 988776655')

    conemail = models.EmailField(
        _('Email contacto'), max_length=255, null=True, blank=True,
        help_text='Solo administración')

    convalor = models.CharField(
        _('Valor'), max_length=10,
        help_text='ej: 100.000')

    conrecordatorio = models.TextField(
        _('Notas y Recordatorios'), null=True, blank=True,
        help_text='Solo administración')

    certificadomedico = models.ImageField(
        _('Certificado Médico'), null=True, blank=True,
        help_text='Subir archivo, solo administración')

    EXAMENMEDICO = (
        ('aldia', 'Al día'),
    )
    examenaldia = models.CharField(
        _('Certificado Médico'), max_length=20, null=True, blank=True,
        choices=EXAMENMEDICO, default='',
        help_text='Usado en sitio')

    ATIENDEUNOS = (
        ('departamentopropio', 'Depto propio'),
    )
    atiendeuno = models.CharField(
        _('Atiende en:'), max_length=20, null=True, blank=True,
        choices=ATIENDEUNOS, default='',
        help_text='Departamento propio')

    ATIENDEDOS = (
        ('hoteles', 'Hoteles'),
    )
    atiendedos = models.CharField(
        _('Atiende en:'), max_length=20, null=True, blank=True,
        choices=ATIENDEDOS, default='',
        help_text='Hoteles')

    ATIENDETRES = (
        ('moteles', 'Moteles'),
    )
    atiendetres = models.CharField(
        _('Atiende en:'), max_length=20, null=True, blank=True,
        choices=ATIENDETRES, default='',
        help_text='Moteles')

    ATIENDECUATRO = (
        ('domicilios', 'Domicilios'),
    )
    atiendecuatro = models.CharField(
        _('Atiende en:'), max_length=20, null=True, blank=True,
        choices=ATIENDECUATRO, default='',
        help_text='Domicilios')

    DIALUNES = (
        ('fulltime', 'Full Time'),
    )
    dialunes = models.CharField(
        _('Lunes'), max_length=20, null=True, blank=True,
        choices=DIALUNES, default='fulltime',
        help_text='')

    DIAMARTES = (
        ('fulltime', 'Full Time'),
    )
    diamartes = models.CharField(
        _('Martes'), max_length=20, null=True, blank=True,
        choices=DIAMARTES, default='fulltime',
        help_text='')

    DIAMIERCOLES = (
        ('fulltime', 'Full Time'),
    )
    diamiercoles = models.CharField(
        _('Miércoles'), max_length=20, null=True, blank=True,
        choices=DIAMIERCOLES, default='fulltime', help_text='')

    DIAJUEVES = (
        ('fulltime', 'Full Time'),
    )
    diajueves = models.CharField(
        _('Jueves'), max_length=20, null=True, blank=True,
        choices=DIAJUEVES, default='fulltime', help_text='')

    DIAVIERNES = (
        ('fulltime', 'Full Time'),
    )
    diaviernes = models.CharField(
        _('Viernes'), max_length=20, null=True, blank=True,
        choices=DIAVIERNES, default='fulltime', help_text='')

    DIASABADO = (
        ('fulltime', 'Full Time'),
    )
    diasabado = models.CharField(
        _('Sábado'), max_length=20, null=True, blank=True,
        choices=DIASABADO, default='fulltime', help_text='')

    DIADOMINGO = (
        ('fulltime', 'Full Time'),
    )
    diadomingo = models.CharField(
        _('Domingo'), max_length=20, null=True, blank=True,
        choices=DIADOMINGO, default='fulltime', help_text='')

    ATENCIONENPAREJA = (
        ('atencionpareja', 'Atención en Pareja'),
    )
    atencion_pareja = models.CharField(
        _('Atención en Pareja'), max_length=24, null=True, blank=True,
        choices=ATENCIONENPAREJA, default='', help_text='')

    ATENCIONAMUEJRES = (
        ('atencionmujeres', 'Atención a Mujeres'),
    )
    atencion_mujeres = models.CharField(
        _('Atención a Mujeres'), max_length=24, null=True, blank=True,
        choices=ATENCIONAMUEJRES, default='', help_text='')

    ATENCIONADISCACI = (
        ('atenciondiscapaci', 'Atención a Discapacitados'),
    )
    atencion_discapaci = models.CharField(
        _('Atención a Discapacitados'), max_length=24, null=True, blank=True,
        choices=ATENCIONADISCACI, default='', help_text='')

    SERVICIOGRIEGO = (
        ('griego', 'Griego'),
    )
    servicio_griego = models.CharField(
        _('Griego'), max_length=24, null=True, blank=True,
        choices=SERVICIOGRIEGO, default='', help_text='')

    FRANCESNATURAL = (
        ('francesnatural', 'Francés Natural'),
    )
    frances_natural = models.CharField(
        _('Francés Natural'), max_length=24, null=True, blank=True,
        choices=FRANCESNATURAL, default='', help_text='')

    SEXOORAL = (
        ('sexooral', 'Sexo Oral'),
    )
    sexo_oral = models.CharField(
        _('Francés Natural'), max_length=24, null=True, blank=True,
        choices=SEXOORAL, default='', help_text='')

    LESBICO = (
        ('lesbico', 'Lésbico'),
    )
    lesbico = models.CharField(
        _('Lésbico'), max_length=24, null=True, blank=True,
        choices=LESBICO, default='', help_text='')

    GARGANTAPROF = (
        ('gargantaproof', 'Garganta Profunda'),
    )
    garganta_profunda = models.CharField(
        _('Garganta Profunda'), max_length=24, null=True, blank=True,
        choices=GARGANTAPROF, default='', help_text='')

    DUALESTRIOS = (
        ('dualestrios', 'Duales o Trios'),
    )
    duales_trios = models.CharField(
        _('Duales o Trios'), max_length=24, null=True, blank=True,
        choices=DUALESTRIOS, default='', help_text='')

    AMERICANAA = (
        ('americana', 'Americana'),
    )
    americanaa = models.CharField(
        _('Americana'), max_length=24, null=True, blank=True,
        choices=AMERICANAA, default='', help_text='')

    AMERICANACORPORAL = (
        ('americanacorporal', 'Americana Corporal'),
    )
    americana_corporal = models.CharField(
        _('Americana Corporal'), max_length=24, null=True, blank=True,
        choices=AMERICANACORPORAL, default='', help_text='')

    MASAJESS = (
        ('masajes', 'Masajes'),
    )
    masajes = models.CharField(
        _('Masajes'), max_length=24, null=True, blank=True,
        choices=MASAJESS, default='', help_text='')

    BAILEEROTICO = (
        ('baileerotico', 'Baile Erótico'),
    )
    baile_erotico = models.CharField(
        _('Baile Erótico'), max_length=24, null=True, blank=True,
        choices=BAILEEROTICO, default='', help_text='')

    BESOSDENOVIA = (
        ('besosdenovia', 'Besos de Novia'),
    )
    besos_novia = models.CharField(
        _('Besos de Novia'), max_length=24, null=True, blank=True,
        choices=BESOSDENOVIA, default='', help_text='')

    JUGUETESEROTIC = (
        ('jugueteserotic', 'Juguetes Eróticos'),
    )
    juguetes_eroticos = models.CharField(
        _('Juguetes Eróticos'), max_length=24, null=True, blank=True,
        choices=JUGUETESEROTIC, default='', help_text='')

    CUADROPLASTICOS = (
        ('cuadroplastico', 'Cuadro Plástico'),
    )
    cuadro_plastico = models.CharField(
        _('Cuadro Plástico'), max_length=24, null=True, blank=True,
        choices=CUADROPLASTICOS, default='', help_text='')

    DESPEDIDASOLTEROS = (
        ('despedidasolteros', 'Despedida de Solteros'),
    )
    despedida_soltero = models.CharField(
        _('Despedida de Solteros'), max_length=24, null=True, blank=True,
        choices=DESPEDIDASOLTEROS, default='', help_text='')

    VIAJESS = (
        ('viajess', 'Viajes'),
    )
    viajess = models.CharField(
        _('Viajes'), max_length=24, null=True, blank=True,
        choices=VIAJESS, default='', help_text='')

    SADISMOSS = (
        ('sadismo', 'Sadismo'),
    )
    sadismo = models.CharField(
        _('Sadismo'), max_length=24, null=True, blank=True,
        choices=SADISMOSS, default='', help_text='')

    servicio_adicional_uno = models.CharField(
        _('Servicio Adicional #1'), max_length=20, null=True, blank=True,
        help_text='')

    servicio_adicional_dos = models.CharField(
        _('Servicio Adicional #2'), max_length=20, null=True, blank=True,
        help_text='')

    servicio_adicional_tres = models.CharField(
        _('Servicio Adicional #3'), max_length=20, null=True, blank=True,
        help_text='')

    servicio_adicional_cuatro = models.CharField(
        _('Servicio Adicional #4'), max_length=20, null=True, blank=True,
        help_text='')

    servicio_adicional_cinco = models.CharField(
        _('Servicio Adicional #5'), max_length=20, null=True, blank=True,
        help_text='')

    servicio_adicional_seis = models.CharField(
        _('Servicio Adicional #6'), max_length=20, null=True, blank=True,
        help_text='')

    servicio_adicional_siete = models.CharField(
        _('Servicio Adicional #7'), max_length=20, null=True, blank=True,
        help_text='')
    servicio_adicional_ocho = models.CharField(
        _('Servicio Adicional #8'), max_length=20, null=True, blank=True,
        help_text='')

    MESESATRABS = (('mes_enero', 'Enero'),
                  ('mes_febrero', 'Febrero'),
                  ('mes_marzo', 'Marzo'),
                  ('mes_abril', 'Abril'),
                  ('mes_mayo', 'Mayo'),
                  ('mes_junio', 'Junio'),
                  ('mes_julio', 'Julio'),
                  ('mes_agosto', 'Agosto'),
                  ('mes_septiembre', 'Septiembre'),
                  ('mes_octubre', 'Octubre'),
                  ('mes_noviembre', 'Noviembre'),
                  ('mes_diciembre', 'Diciembre')
    )
    mesesatra = MultiSelectField(
        _('Registro de meses'), null=True, blank=True,
        choices=MESESATRABS, help_text='Solo administración')
    edad = models.CharField(
        max_length=2, default=16, null=True, blank=True,
        choices=((str(x), x) for x in range(16, 61)), help_text='Rango de edad')
    nacionalidad = models.CharField(
        _('Nacionalidad'), max_length=20, help_text='Pais de orígen')
    TIPOS_PIEL = (
        ('blanca', 'Blanca'),
        ('trigueña', 'Trigueña'),
        ('morena', 'Morena'),
    )
    tez = models.CharField(
        max_length=20, null=True, blank=True,
        choices=TIPOS_PIEL, default='blanca',
        help_text='Tipo de piel')
    altura = models.CharField(
        max_length=3, default=120, null=True, blank=True,
        choices=((str(x), x) for x in range(120, 201)),
        help_text='Altura en centímetros')
    peso = models.CharField(
        max_length=2, default=40, null=True, blank=True,
        choices=((str(x), x) for x in range(40, 91)),
        help_text='Peso en kilogramos')
    busto = models.CharField(
        max_length=3, default=40, null=True, blank=True,
        choices=((str(x), x) for x in range(40, 181)),
        help_text='(X) Medida de busto en centímetros (X)')
    cintura = models.CharField(
        max_length=3, default=40, null=True, blank=True,
        choices=((str(x), x) for x in range(40, 181)),
        help_text='(Z) Medida de cintura en centímetros (Z)')
    cadera = models.CharField(
        max_length=3, default=40, null=True, blank=True,
        choices=((str(x), x) for x in range(40, 181)),
        help_text='(Y) Medida de cadera en centímetros (Y)')
    TIPOS_CONTEXTURA = (
        ('flaca', 'Flaca'),
        ('delgada', 'Delgada'),
        ('atletica', 'Atlética'),
        ('promedio', 'Promedio'),
        ('gruesa', 'Gruesa'),
        ('vuluptuosa', 'Vuluptuosa'),
        ('gorda', 'Gorda')
    )
    contextura = models.CharField(
        max_length=20, null=True, blank=True,
        choices=TIPOS_CONTEXTURA, default='flaca', help_text='Tipo de cuerpo')
    COLOR_CABELLO = (
        ('negro', 'Negro'),
        ('castano', 'Castaño'),
        ('chocolate', 'Chocolate'),
        ('rubio', 'Rubio'),
        ('cobrizo', 'Cobrizo')
    )
    cabello = models.CharField(
        max_length=20, null=True, blank=True,
        choices=COLOR_CABELLO, default='negro', help_text='Color de cabello')
    COLOR_OJOS = (
        ('marrones', 'Marrones'),
        ('avellana', 'Avellana'),
        ('miel', 'Miel'),
        ('verdes', 'Verdes'),
        ('azulmar', 'Azul Mar'),
        ('azules', 'Azules')
    )
    ojos = models.CharField(
        max_length=20, null=True, blank=True,
        choices=COLOR_OJOS, default='marrones', help_text='Color de ojos')
    MEDIDA_BUSTO = (
        ('pequeño', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
        ('muygrande', 'Muy grande')
    )
    busto2 = models.CharField(
        _('Tipo de busto'), max_length=20, null=True, blank=True,
        choices=MEDIDA_BUSTO, default='pequeño', help_text='Tipo de busto')
    MEDIDA_COLA = (
        ('pequeña', 'Pequeña'),
        ('mediana', 'Mediana'),
        ('grande', 'Grande'),
        ('muygrande', 'Muy grande')
    )
    cola = models.CharField(
        _('Tipo de cola'), max_length=20, null=True, blank=True,
        choices=MEDIDA_COLA, default='pequeña', help_text='Tipo de cola')
    TIPO_DEPILACION = (
        ('sindepilar', 'Sin Depilar'),
        ('comun', 'Común'),
        ('cavadofrances', 'Cavado francés'),
        ('cavadotanga', 'Cavado de tanga'),
        ('cajatiffany', 'Caja tiffany'),
        ('brasileñototal', 'Brasileño total'),
        ('completa', 'Depilada Completa')
    )
    depilacion = models.CharField(
        _('Depilación'), max_length=20, null=True, blank=True,
        choices=TIPO_DEPILACION, default='sindepilar', help_text='Tipo de depilación')
    CIUDADLISTA = (
        ('rancagua', 'Rancagua'),
        ('curico', 'Curicó'),
        ('talca', 'Talca '),
        ('concepción', 'Concepción'),
        ('chillan', 'Chillán'),
        ('losangeles', 'Los Angeles'),
        ('temuco', 'Temuco'),
        ('pucon', 'Pucón'),
        ('valdivia', 'Valdivia'),
        ('osorno', 'Osorno'),
        ('puertomontt', 'Puerto Montt'),
        ('castro', 'Castro'),
    )
    ciudadheader = models.CharField(
        _('Encabezado'), max_length=20, null=True, blank=True,
        choices=CIUDADLISTA, default='', help_text='Seleccione la ciudad para el encabezado de perfil ')
    IDIOMAUNO = (
        ('espanol', 'Español'),
        ('ingles', 'Inglés'),
        ('portugues', 'Portugués '),
        ('ruso', 'Ruso'),
        ('aleman', 'Alemán'),
        ('frances', 'Frances')
    )
    idiomauno = models.CharField(
        _('Idioma Principal'), max_length=20, null=True, blank=True,
    choices=IDIOMAUNO, default='espanol', help_text='Idioma Principal')
    IDIOMADOS = (
        ('espanol', 'Español'),
        ('ingles', 'Inglés'),
        ('portugues', 'Portugués '),
        ('ruso', 'Ruso'),
        ('aleman', 'Alemán'),
        ('frances', 'Francés')
    )
    idiomados = models.CharField(
        _('Idioma Secundario'), max_length=20, null=True, blank=True,
        choices=IDIOMADOS, default='', help_text='Idioma Secundario')

    modeloretoque = models.CharField(
        _('Comentario Retoque'), max_length=255, null=True, blank=True, help_text='ej: ha sido entrevistada personalmente, sus fotografías están levemente retocadas')

    def get_imagen_box(instance, filename):
        now = datetime.datetime.now()
        return '/'.join([
            now.strftime('%Y'),
            now.strftime('%m'),
            now.strftime('%d'),
            instance.slug, 'box', filename])
    def get_imagen_perfil(instance, filename):
        now = datetime.datetime.now()
        return '/'.join([
            now.strftime('%Y'),
            now.strftime('%m'),
            now.strftime('%d'),
            instance.slug, 'perfil', filename])
    def get_imagen_galeria(instance, filename):
        now = datetime.datetime.now()
        return '/'.join([
            now.strftime('%Y'),
            now.strftime('%m'),
            now.strftime('%d'),
            instance.slug, 'galeria', filename])
    image = models.ImageField(
        _('Imagen de caja'), upload_to=get_imagen_box,
        help_text=_('Usada para portada'))
    image2 = models.ImageField(
        _('Imagen de Perfil'), upload_to=get_imagen_perfil,
        help_text='Usada para perfil')
    imagal1 = models.ImageField(
        _('Imagen de Galeria (1)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 1')
    imagal2 = models.ImageField(
        _('Imagen de Galeria (2)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 2')
    imagal3 = models.ImageField(
        _('Imagen de Galeria (3)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 3')
    imagal4 = models.ImageField(
        _('Imagen de Galeria (4)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 4')
    imagal5 = models.ImageField(
        _('Imagen de Galeria (5)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 5')
    imagal6 = models.ImageField(
        _('Imagen de Galeria (6)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 6')
    imagal7 = models.ImageField(
        _('Imagen de Galeria (7)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 7')
    imagal8 = models.ImageField(
        _('Imagen de Galeria (8)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 8')
    imagal9 = models.ImageField(
        _('Imagen de Galeria (9)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 9')
    imagal10 = models.ImageField(
        _('Imagen de Galeria (10)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 10')
    imagal11 = models.ImageField(
        _('Imagen de Galeria (11)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 11')
    imagal12 = models.ImageField(
        _('Imagen de Galeria (12)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 12')
    imagal13 = models.ImageField(
        _('Imagen de Galeria (13)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 13')
    imagal14 = models.ImageField(
        _('Imagen de Galeria (14)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 14')
    imagal15 = models.ImageField(
        _('Imagen de Galeria (15)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 15')
    imagal16 = models.ImageField(
        _('Imagen de Galeria (16)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 16')
    imagal17 = models.ImageField(
        _('Imagen de Galeria (17)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 17')
    imagal18 = models.ImageField(
        _('Imagen de Galeria (18)'), upload_to=get_imagen_galeria,
        null=True, blank=True, help_text='Imagen 18')

    CATEGORIASS = (
        ('vip', 'Vip'),
        ('premium', 'Premium'),
        ('gold', 'Gold '),
        ('silver', 'Silver')
    )
    categoriass = models.CharField(
        _('Categoría'), max_length=20, null=True, blank=True,
        choices=CATEGORIASS, default='', help_text='Categoria')


    slug = models.SlugField(
        _('slug'), unique=True, max_length=255,
        unique_for_date='publication_date',
        help_text=_("Used to build the entry's URL."))



    status = models.IntegerField(
        _('status'), db_index=True, choices=STATUS_CHOICES, default=DRAFT,
        help_text='Borrador: en edición / Oculto: almacenado / Publicado: en sitio')
    publication_date = models.DateTimeField(
        _('publication date'),
        db_index=True, default=timezone.now,
        help_text=_("Used to build the entry's URL."))

    start_publication = models.DateTimeField(
        _('start publication'),
        db_index=True, blank=True, null=True,
        help_text=_('Start date of publication.'))

    end_publication = models.DateTimeField(
        _('end publication'),
        db_index=True, blank=True, null=True,
        help_text=_('End date of publication.'))

    sites = models.ManyToManyField(
        Site,
        related_name='entries',
        verbose_name=_('sites'),
        help_text=_('Sites where the entry will be published.'))

    creation_date = models.DateTimeField(
        _('creation date'),
        default=timezone.now)

    last_update = models.DateTimeField(
        _('last update'), default=timezone.now)

    objects = models.Manager()

    published = EntryPublishedManager()

    @property
    def is_actual(self):
        """
        Checks if an entry is within his publication period.
        """
        now = timezone.now()
        if self.start_publication and now < self.start_publication:
            return False

        if self.end_publication and now >= self.end_publication:
            return False
        return True

    @property
    def is_visible(self):
        """
        Checks if an entry is visible and published.
        """
        return self.is_actual and self.status == PUBLISHED

    @property
    def previous_entry(self):
        """
        Returns the previous published entry if exists.
        """
        return self.previous_next_entries[0]

    @property
    def next_entry(self):
        """
        Returns the next published entry if exists.
        """
        return self.previous_next_entries[1]

    @property
    def previous_next_entries(self):
        """
        Returns and caches a tuple containing the next
        and previous published entries.
        Only available if the entry instance is published.
        """
        previous_next = getattr(self, 'previous_next', None)

        if previous_next is None:
            if not self.is_visible:
                previous_next = (None, None)
                setattr(self, 'previous_next', previous_next)
                return previous_next

            entries = list(self.__class__.published.all())
            index = entries.index(self)
            try:
                previous = entries[index + 1]
            except IndexError:
                previous = None

            if index:
                _next = entries[index - 1]
            else:
                _next = None
            previous_next = (previous, _next)
            setattr(self, 'previous_next', previous_next)
        return previous_next

    @property
    def short_url(self):
        """
        Returns the entry's short url.
        """
        return get_url_shortener()(self)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to update the
        the last_update field.
        """
        self.last_update = timezone.now()
        super(CoreEntry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Builds and returns the entry's URL based on
        the slug and the creation date.
        """
        publication_date = self.publication_date
        if timezone.is_aware(publication_date):
            publication_date = timezone.localtime(publication_date)
        return reverse('zinnia:entry_detail', kwargs={
            'year': publication_date.strftime('%Y'),
            'month': publication_date.strftime('%m'),
            'day': publication_date.strftime('%d'),
            'slug': self.slug})

    def __str__(self):
        return '%s: %s' % (self.title, self.get_status_display())

    class Meta:
        """
        CoreEntry's meta informations.
        """
        abstract = True
        ordering = ['-publication_date']
        get_latest_by = 'publication_date'
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        index_together = [['slug', 'publication_date'],
                          ['status', 'publication_date',
                           'start_publication', 'end_publication']]
        permissions = (('can_view_all', 'Can view all entries'),
                       ('can_change_status', 'Can change status'),
                       ('can_change_author', 'Can change author(s)'), )

class ContentEntry(models.Model):
    """
    Abstract content model class providing field
    and methods to write content inside an entry.
    """
    content = models.TextField(_('Descripción'), blank=True)

    @property
    def html_content(self):
        """
        Returns the "content" field formatted in HTML.
        """
        return html_format(self.content)

    @property
    def html_preview(self):
        """
        Returns a preview of the "content" field or
        the "lead" field if defined, formatted in HTML.
        """
        return HTMLPreview(self.html_content,
                           getattr(self, 'html_lead', ''))

    @property
    def word_count(self):
        """
        Counts the number of words used in the content.
        """
        return len(strip_tags(self.html_content).split())

    class Meta:
        abstract = True

class DiscussionsEntry(models.Model):
    """
    Abstract discussion model class providing
    the fields and methods to manage the discussions
    (comments, pingbacks, trackbacks).
    """
    comment_enabled = models.BooleanField(
        _('comments enabled'), default=True,
        help_text=_('Allows comments if checked.'))
    pingback_enabled = models.BooleanField(
        _('pingbacks enabled'), default=True,
        help_text=_('Allows pingbacks if checked.'))
    trackback_enabled = models.BooleanField(
        _('trackbacks enabled'), default=True,
        help_text=_('Allows trackbacks if checked.'))

    comment_count = models.IntegerField(
        _('comment count'), default=0)
    pingback_count = models.IntegerField(
        _('pingback count'), default=0)
    trackback_count = models.IntegerField(
        _('trackback count'), default=0)

    @property
    def discussions(self):
        """
        Returns a queryset of the published discussions.
        """
        return comments.get_model().objects.for_model(
            self).filter(is_public=True, is_removed=False)

    @property
    def comments(self):
        """
        Returns a queryset of the published comments.
        """
        return self.discussions.filter(Q(flags=None) | Q(
            flags__flag=CommentFlag.MODERATOR_APPROVAL))

    @property
    def pingbacks(self):
        """
        Returns a queryset of the published pingbacks.
        """
        return self.discussions.filter(flags__flag=PINGBACK)

    @property
    def trackbacks(self):
        """
        Return a queryset of the published trackbacks.
        """
        return self.discussions.filter(flags__flag=TRACKBACK)

    def discussion_is_still_open(self, discussion_type, auto_close_after):
        """
        Checks if a type of discussion is still open
        are a certain number of days.
        """
        discussion_enabled = getattr(self, discussion_type)
        if (discussion_enabled and isinstance(auto_close_after, int) and
                auto_close_after >= 0):
            return (timezone.now() - (
                self.start_publication or self.publication_date)).days < \
                auto_close_after
        return discussion_enabled

    @property
    def comments_are_open(self):
        """
        Checks if the comments are open with the
        AUTO_CLOSE_COMMENTS_AFTER setting.
        """
        return self.discussion_is_still_open(
            'comment_enabled', AUTO_CLOSE_COMMENTS_AFTER)

    @property
    def pingbacks_are_open(self):
        """
        Checks if the pingbacks are open with the
        AUTO_CLOSE_PINGBACKS_AFTER setting.
        """
        return self.discussion_is_still_open(
            'pingback_enabled', AUTO_CLOSE_PINGBACKS_AFTER)

    @property
    def trackbacks_are_open(self):
        """
        Checks if the trackbacks are open with the
        AUTO_CLOSE_TRACKBACKS_AFTER setting.
        """
        return self.discussion_is_still_open(
            'trackback_enabled', AUTO_CLOSE_TRACKBACKS_AFTER)

    class Meta:
        abstract = True


class RelatedEntry(models.Model):
    """
    Abstract model class for making manual relations
    between the differents entries.
    """
    related = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name=_('related entries'))

    @property
    def related_published(self):
        """
        Returns only related entries published.
        """
        return entries_published(self.related)

    class Meta:
        abstract = True

class LeadEntry(models.Model):
    """
    Abstract model class providing a lead content to the entries.
    """
    lead = models.TextField(
        _('lead'), blank=True,
        help_text=_('Lead paragraph'))

    @property
    def html_lead(self):
        """
        Returns the "lead" field formatted in HTML.
        """
        return html_format(self.lead)

    class Meta:
        abstract = True

class ExcerptEntry(models.Model):
    """
    Abstract model class to add an excerpt to the entries.
    """
    excerpt = models.TextField(
        _('excerpt'), blank=True,
        help_text=_('Used for SEO purposes.'))

    def save(self, *args, **kwargs):
        """
        Overrides the save method to create an excerpt
        from the content field if void.
        """
        if not self.excerpt and self.status == PUBLISHED:
            self.excerpt = Truncator(strip_tags(
                getattr(self, 'content', ''))).words(50)
        super(ExcerptEntry, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class FeaturedEntry(models.Model):
    """
    Abstract model class to mark entries as featured.
    """
    featured = models.BooleanField(
        _('featured'), default=False)

    class Meta:
        abstract = True

class AuthorsEntry(models.Model):
    """
    Abstract model class to add relationship
    between the entries and their authors.
    """
    authors = models.ManyToManyField(
        'zinnia.Author',
        blank=True,
        related_name='entries',
        verbose_name=_('authors'))

    class Meta:
        abstract = True

class CategoriesEntry(models.Model):
    """
    Abstract model class to categorize the entries.
    """
    categories = models.ManyToManyField(
        'zinnia.Category',
        blank=True,
        related_name='entries',
        verbose_name=_('ciudad'))

    class Meta:
        abstract = True

class TagsEntry(models.Model):
    """
    Abstract model class to add tags to the entries.
    """
    tags = TagField(_('tags'))

    @property
    def tags_list(self):
        """
        Return iterable list of tags.
        """
        return parse_tag_input(self.tags)

    class Meta:
        abstract = True

class LoginRequiredEntry(models.Model):
    """
    Abstract model class to restrcit the display
    of the entry on authenticated users.
    """
    login_required = models.BooleanField(
        _('login required'), default=False,
        help_text=_('Only authenticated users can view the entry.'))

    class Meta:
        abstract = True

class PasswordRequiredEntry(models.Model):
    """
    Abstract model class to restrict the display
    of the entry to users knowing the password.
    """
    password = models.CharField(
        _('password'), max_length=50, blank=True,
        help_text=_('Protects the entry with a password.'))

    class Meta:
        abstract = True

class ContentTemplateEntry(models.Model):
    """
    Abstract model class to display entry's content
    with a custom template.
    """
    content_template = models.CharField(
        _('content template'), max_length=250,
        default='zinnia/_entry_detail.html',
        choices=[('zinnia/_entry_detail.html', _('Default template'))] +
        ENTRY_CONTENT_TEMPLATES,
        help_text=_("Template used to display the entry's content."))

    class Meta:
        abstract = True

class DetailTemplateEntry(models.Model):
    """
    Abstract model class to display entries with a
    custom template if needed on the detail page.
    """
    detail_template = models.CharField(
        _('detail template'), max_length=250,
        default='entry_detail.html',
        choices=[('entry_detail.html', _('Default template'))] +
        ENTRY_DETAIL_TEMPLATES,
        help_text=_("Template used to display the entry's detail page."))

    class Meta:
        abstract = True

class AbstractEntry(
        CoreEntry,
        ContentEntry,
        DiscussionsEntry,
        RelatedEntry,
        LeadEntry,
        ExcerptEntry,
        FeaturedEntry,
        AuthorsEntry,
        CategoriesEntry,
        TagsEntry,
        LoginRequiredEntry,
        PasswordRequiredEntry,
        ContentTemplateEntry,
        DetailTemplateEntry):
    """
    Final abstract entry model class assembling
    all the abstract entry model classes into a single one.

    In this manner we can override some fields without
    reimplemting all the AbstractEntry.
    """

    class Meta(CoreEntry.Meta):
        abstract = True