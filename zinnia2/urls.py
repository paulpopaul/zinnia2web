"""zinnia2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from django.conf.urls.static import static
from . import views
from zinnia2 import  settings
from zinniablog2.views import IndexView, PerfilDetailView


urlpatterns = [
    path('admin/', admin.site.urls),


    path('dir/', include('zinnia.urls')),
    path('dir/ciudad/', include('zinnia.urls.categories')),
    path('blog/', include('zinnia.urls.entries')),
    path('search/', include('zinnia.urls.search')),
    path('sitemap/', include('zinnia.urls.sitemap')),
    path('comments/', include('django_comments.urls')),


    path('', IndexView.as_view(), name='index'),
    path('caca/<slug:slug>/', PerfilDetailView.as_view()),
    path('contacto/', views.contacto, name='contacto'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
