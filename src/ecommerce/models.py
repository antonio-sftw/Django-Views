from django.db import models # type: ignore

# Create your models here.
from .validators import validate_blocked_words # Importar función propia
from base.models import BasePublicado # Importar clase abstracta para estado de publicación
from django.db.models import signals # type: ignore # Importar el módulo signals para manejar señales
from django.utils.text import slugify # type: ignore # Importar el módulo slugify para crear un slug a partir de un texto
from django.conf import settings # type: ignore # Importar el módulo settings para obtener la configuración de la aplicación

User = settings.AUTH_USER_MODEL # Obtener el modelo de usuario

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
    slug = models.SlugField(null=True, blank=True, db_index=True)
    # Relación con el modelo User, se elimina el usuario y todos los productos asociados
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
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

    # Métodos

    def obtener_url(self):
        return f"/ecommerce/producto/{self.slug}"

# Clase ProductoDigital que hereda de Producto, es un proxy para Producto
class ProductoDigital(Producto):
    class Meta:
        proxy = True
    
# Esta función se ejecuta automáticamente antes de guardar un producto
# Genera un slug único a partir del nombre del producto, está fuera del modelo
def slug_pre_save(sender, instance, *args, **kwargs):
    # Si el slug está vacío o es None
    if instance.slug is None or instance.slug == "":
        # Convierte el nombre en un slug (texto en minúsculas, sin espacios ni caracteres especiales)
        nuevo_slug = slugify(instance.nombre)
        
        # Obtiene el modelo actual (Producto)
        modelo = instance.__class__
        
        # Busca productos que tengan un slug que empiece igual
        # Excluye el producto actual (para actualizaciones)
        registros = modelo.objects.filter(slug__startswith=nuevo_slug).exclude(id=instance.id)
        
        # Si no hay otros productos con slug similar
        if registros.count() == 0:
            instance.slug = nuevo_slug
        else:
            # Si hay otros productos similares, añade un número al final
            # Ejemplo: producto, producto-2, producto-3
            instance.slug = f"{nuevo_slug}-{registros.count() + 1}"

# Conecta la función al evento pre_save del modelo Producto
# Se ejecutará automáticamente antes de guardar cualquier producto
signals.pre_save.connect(slug_pre_save, sender=Producto)