from django.contrib import admin # type: ignore

# Register your models here.
from .models import Producto

admin.site.register(Producto)  # Registra el modelo Producto en el admin
