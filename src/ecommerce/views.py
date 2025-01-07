# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Producto # Importar el modelo Producto a la vista

def home(request):
    # return HttpResponse("<h1>Hola mundo</h1>")

    # html = """
    #     <!DOCTYPE html>
    #     <html lang="en">
    #     <head>
    #         <meta charset="UTF-8">
    #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #         <title>Document</title>

    #         <style>
    #             h1 {
    #                 color: blue;
    #             }
    #         </style>
    #     </head>
    #     <body>
    #         <h1>Hola mundo</h1>
    #     </body>
    #     </html>
    # """
    # return HttpResponse(html)

    # productos = Producto.objects.all() # Obtener todos los productos
    # return HttpResponse(productos)

    # Usando templates
    
    productos = Producto.objects.all() # Obtener todos los productos
    
    template = "ecommerce/list-view.html"
    
    # Contexto de la vista, se le pasan los datos que se van a mostrar en el template
    context = {
        # "request": request,
        "titulo": "Productos",
        "items": productos
    }

    return render(request, template, context) # Renderiza el template con los datos del contexto

# Modulo importado para redireccionar a otra pagina
def redirect_to_about(request):
    return HttpResponseRedirect("/about")
