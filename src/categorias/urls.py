from django.urls import path # type: ignore
from django.contrib import admin # type: ignore
from django.views.generic import TemplateView, RedirectView # type: ignore

from categorias.views import CategoriaHomeView, CategoriaListView, CategoriaDetailView # Importar las clases de las vistas

urlpatterns = [
    # path("home", CategoriaHomeView.as_view(), name="home"),
    path("", CategoriaListView.as_view(), name="list"),
    path("<int:pk>", CategoriaDetailView.as_view(), name="detail"),
    path("about", TemplateView.as_view(template_name="about.html")), # Ejemplo de TemplateView
    path("about-us", RedirectView.as_view(url="/categorias/about")), # Ejemplo de redireccionamiento con RedirectView
]
