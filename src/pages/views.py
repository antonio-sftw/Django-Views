import os

from django import get_version # type: ignore
from django.conf import settings # type: ignore
from django.shortcuts import render # type: ignore


def home(request):
    class Producto:
        def __init__(self, nombre, precio, descripcion):
            self.nombre = nombre
            self.precio = precio
            self.descripcion = descripcion

        def calcular_total(self, cantidad):
            return self.precio * cantidad

    class ProductoInternacional(Producto):
        def __init__(self, nombre, precio, descripcion, tasa_internacional):
            self.nombre = nombre
            self.precio = precio
            self.descripcion = descripcion
            self.tasa_internacional = tasa_internacional
        
        def calcular_total_con_tasa(self, cantidad):
            total = self.calcular_total(cantidad) # Llama al método que heredó de Producto dentro de su propio método nuevo
            total += total * self.tasa_internacional # Se agrega al total el resultado del total por el impuesto extra
            return total

    producto = Producto("Camiseta", 50.0, "Camiseta de algodón")

    print(f"Compra de {producto.nombre}")
    print(f"total: ${producto.calcular_total(10)}")

    producto_internacional = ProductoInternacional("Audífonos", 100.0, "Audífonos", 0.2)

    print(f"Compra de {producto_internacional.nombre}")
    print(f"total: ${producto_internacional.calcular_total(10)}")
    print(f"total con tasa internacional: ${producto_internacional.calcular_total_con_tasa(10)}")

    context = {
        "debug": settings.DEBUG,
        "django_ver": "Version: {}".format(get_version()),
        "python_ver": "Version: {}".format( os.environ["PYTHON_VERSION"]),
        "producto": "Compra de {}, total: ${}".format(producto.nombre, producto.calcular_total(10)),
        "producto_internacional": "Compra de {}, total: ${}, total con tasa internacional: ${}".format(producto_internacional.nombre, producto_internacional.calcular_total(10), producto_internacional.calcular_total_con_tasa(10))
    }

    return render(request, "pages/home.html", context)
