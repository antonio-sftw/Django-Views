from django import forms
from .models import Producto

# Clase para crear un formulario del modelo Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "precio", "descripcion"]