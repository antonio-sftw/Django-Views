from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=100, null=True)
    descripcion = models.TextField()
    dimensiones = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=100, null=True)
    
    stock = models.PositiveIntegerField(default=0)
    codigo_barras = models.CharField(max_length=13, unique=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    # categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    # imagen = models.ImageField(upload_to="productos")
