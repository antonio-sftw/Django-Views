from django.db import models # type: ignore

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    slug = models.SlugField(null=True, blank=True, db_index=True)
