from django.shortcuts import render # type: ignore

# Create your views here.
from django.views.generic import ListView, View, TemplateView, DetailView # type: ignore
# from django.decorators.http import require_http_methods # type: ignore

from .models import Categoria

class CategoriaHomeView(View):
    def get(request, self, *args, **kwargs):
        return render(request, "categorias/home.html")
    
    # def post(request, self, *args, **kwargs):
    #     return render(request, "categorias/list-view.html")
    
class CategoriaListView(ListView):
    # Pasándole este atributo, django busca el template en categorias/categoria_list.html
    model = Categoria

    # Sobre escribir el método get_context_data de ListView
    def get_context_data(self, *args, **kwargs):
        # Llamar al método de la clase padre, devuelve un diccionario con los datos y registros del modelo
        context = super().get_context_data(*args, **kwargs)
        context["titulo"] = "Categorias"
        return context

class CategoriaDetailView(DetailView):
    model = Categoria

# *********************************************************************************************************************************************

# Vista basada en funciones

# def about_us_view(request):
#     template = "categorias/about.html"
    # context = {
    #     "titulo": "Acerca de nosotros",
    #     "items": "items",
    # }
#     return render(request, template, context)

# Vista basada en clases

# class AboutView(View):
#     def get(self, request, *args, **kwargs):
#         template = "categorias/about.html"
#         context = {
#             "titulo": "Acerca de nosotros",
#             "items": "items",
#         }
#         return render(request, template, context)

# Vista basada en clases con TemplateView

# class AboutView(TemplateView):
#     template_name = "about.html"

# Simplificada aun mas, se puede declarar directamente el template en el urls.py