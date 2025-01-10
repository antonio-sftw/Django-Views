from django.db import models

# Create your models here.
from .validators import validate_blocked_words # Importar función propia
from base.models import BasePublicado # Importar clase abstracta para estado de publicación

# Clase Producto que hereda de BasePublicado para tener el estado de publicación, tiene todos sus atributos y métodos
class Producto(BasePublicado):
    # Opciones de colores para el producto, se crea una clase interna para que sea accesible desde el modelo, esta hereda de TextChoices
    class ColoresProductoOpciones(models.TextChoices):
        BLANCO = 'BL', 'Blanco'
        NEGRO = 'NG', 'Negro'
        ROJO = 'RJ', 'Rojo'
        AZUL = 'AZ', 'Azul'
        VERDE = 'VR', 'Verde'
        AMARILLO = 'AM', 'Amarillo'
    
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=100, null=True)
    descripcion = models.TextField()
    dimensiones = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=2, choices=ColoresProductoOpciones.choices, null=True)
    stock = models.PositiveIntegerField(default=0)
    codigo_barras = models.CharField(max_length=13, unique=True, null=True)
    estado = models.BooleanField(choices=[(True, 'Activo'), (False, 'Inactivo')], default=True)

    # Ya no se necesita, se hereda de BasePublicado
    # fecha_creacion = models.DateTimeField(auto_now_add=True)
    # fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # TODO: Añadir los campos de proveedor y categoría
    # proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    # categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    # imagen = models.ImageField(upload_to="productos")

    # Polimorfismo, sobre escribir el método heredado save de la clase padre Model para añadir la validación extra
    # Args y kwargs permite que la función reciba cualquier cantidad de parámetros
    def save(self, *args, **kwargs):
        validate_blocked_words(self.nombre)
        # Manda a llamar a la función de la clase padre y guarda el registro después de la validación
        super().save(*args, **kwargs)