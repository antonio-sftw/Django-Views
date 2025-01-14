from django import forms # type: ignore
from .models import Producto

# Clase para crear un formulario del modelo Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "precio", "marca", "descripcion", "dimensiones", "color", "stock", "codigo_barras", "estado", "estado_publicacion", "usuario"]