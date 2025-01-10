# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404 # Importar la función get_object_or_404 para obtener un objeto o devolver un error 404 si no existe

from django.contrib import messages # Importar el módulo messages para mostrar mensajes de éxito, error, etc.
from django.contrib.auth.decorators import login_required # Importar el decorador para verificar si el usuario está autenticado
from .forms import ProductoForm # Importar el formulario ProductoForm
from .models import Producto # Importar el modelo Producto 
from django.db.models import Q # Importar el módulo Q para realizar consultas complejas

def home(request):
    # return HttpResponse("<h1>Hola mundo</h1>")

    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>

            <style>
                h1 {
                    color: blue;
                }
            </style>
        </head>
        <body>
            <h1>Hola mundo</h1>
        </body>
        </html>
    """
    return HttpResponse(html)

def list_products(request):
    # productos = Producto.objects.all() # Obtener todos los productos, el método devuelve una lista de todos los objetos del modelo
    # return HttpResponse(productos)

    # Usando templates

    # Verificar si el usuario está autenticado para mostrar el template correcto
    # if request.user.is_authenticated:
    #     template = "ecommerce/list-view.html"
    # else:
    #     template = "ecommerce/list-view-public.html"

    # Template dinámico para no usar dos templates
    template = "ecommerce/list-view.html"

    # Obtener el valor del query de la URL, si no existe (no se hizo ninguna búsqueda), se asigna None
    query = request.GET.get('query' or None)

    if query:
        # Filtrar los productos que coincidan con el valor por el nombre y/o descripción
        productos = Producto.objects.filter(Q(nombre__icontains=query) | Q(marca__icontains=query) | Q(descripcion__icontains=query) | Q(color__icontains=query))

        activos = Producto.objects.filter(estado=True)

        context = {
            "titulo": "Resultados de la búsqueda",
            "items": productos,
            "items_activos": activos,
            "link_text": "Volver a la lista"
        }

        return render(request, template, context)
    
    productos = Producto.objects.all()
    activos = Producto.objects.filter(estado=True)
    
    # Contexto de la vista, se le pasan los datos que se van a mostrar en el template
    context = {
        "titulo": "Productos",
        "items": productos,
        "items_activos": activos
    }

    return render(request, template, context) # Renderiza el template con los datos del contexto

def detail_products(request, product_id):
    producto = get_object_or_404(Producto, id=product_id) # Obtener el objeto (producto) por su id 
    
    template = "ecommerce/detail-view.html"
    
    context = {
        "titulo": "Producto",
        "items": producto
    }

    return render(request, template, context)

# Decorador para verificar si el usuario está autenticado, si no lo redirige a la página de login, la constante LOGIN_REDIRECT_URL se encuentra en el archivo settings.py
@login_required
def create_products(request):
    # Crea una instancia del formulario ProductoForm si el request es POST, si no es POST, crea una instancia vacía
    form = ProductoForm(request.POST or None)

    # Valida automáticamente el formulario en base a las especificaciones de los atributos del modelo Producto
    if form.is_valid():
        # Crea una instancia del modelo Producto con los datos del formulario pero no la guarda en la base de datos por si necesita modificarse
        producto = form.save(commit=False)
        # producto.nombre = "Producto 1"
        
        producto.save()
        # Muestra un mensaje de éxito y redirige a la página de listado
        messages.success(request, "Producto creado correctamente")
        return HttpResponseRedirect("/ecommerce/productos")
    
    template = "ecommerce/form-view.html"
    
    context = {
        "titulo": "Crear Producto",
        "form": form,
        "button_text": "Guardar"
    }

    return render(request, template, context)

@login_required
def update_products(request, product_id = None):
    producto = get_object_or_404(Producto, id=product_id)

    #  Toma de parámetro adicional el objeto (producto) para que el formulario se pre-rellene con los datos del producto
    form = ProductoForm(request.POST or None, instance=producto)

    if form.is_valid():
        producto_actualizado = form.save(commit=False)
        producto_actualizado.save()
        messages.success(request, "Producto actualizado correctamente")
        return HttpResponseRedirect("/ecommerce/productos")

    template = "ecommerce/form-view.html"
    
    context = {
        "titulo": "Actualizar Producto",
        "form": form,
        "button_text": "Editar"
    }
    
    return render(request, template, context)

@login_required
def delete_products(request, product_id = None):
    producto = get_object_or_404(Producto, id=product_id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente")
    return HttpResponseRedirect("/ecommerce/productos")

# Modulo importado para redireccionar a otra pagina
def redirect_to_about(request):
    return HttpResponseRedirect("/about")