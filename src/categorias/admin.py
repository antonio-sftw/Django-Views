from django.contrib import admin # type: ignore

# Register your models here.
from .models import Categoria

admin.site.register(Categoria)  # Registra el modelo Categoria en el admin