from django.db import models

# Create your models here.
from django.utils import timezone # Importar timezone para obtener la fecha y hora actual

# Clase abstracta para cualquier registro que tenga estado de publicación, nunca se creará un objeto de esta clase
class BasePublicado(models.Model):
    # Meta para que el modelo sea abstracto y no se cree en la base de datos
    class Meta:
        abstract = True
        # Ordenar los registros por fecha de creación y actualización, el signo menos (-) indica que se ordena de forma descendente
        ordering = ['-fecha_actualizacion', '-fecha_creacion']

    # Opciones de estados, se crea una clase interna para que sea accesible desde el modelo, esta hereda de TextChoices
    class EstadoPublicacionOpciones(models.TextChoices):
        PUBLICADO = 'PUB', 'Publicado'
        BORRADOR = 'BOR', 'Borrador'
        PRIVADO = 'PRI', 'Privado'

    estado_publicacion = models.CharField(max_length=3, choices=EstadoPublicacionOpciones.choices, default=EstadoPublicacionOpciones.BORRADOR)
    # auto_now_add:
        # Se establece SOLO UNA VEZ al crear el objeto
        # No cambia aunque el objeto se modifique después
        # Perfecto para "fecha de creación"
    # auto_now:
        # Se actualiza CADA VEZ que se llama a .save()
        # Cambia automáticamente con cada modificación
        # Ideal para "última actualización"
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    
    # Método para verificar si el registro está publicado, esta destinado a ser usado como property
    @property
    def estado_publicacion_esta_publicado(self):
        return self.estado_publicacion == self.EstadoPublicacionOpciones.PUBLICADO
    
    def esta_publicado(self):
        # Retorna True solo si:
        # 1. El estado_publicacion es "PUBLICADO" (verificado por el property estado_publicacion_esta_publicado)
        # 2. La fecha de publicación es anterior a la fecha/hora actual
        return self.estado_publicacion_esta_publicado and self.fecha_publicacion < timezone.now()

    # Polimorfismo, sobre escribir el método heredado save de la clase padre Model
    def save(self, *args, **kwargs):
        # Si el estado es "PUBLICADO" y no tiene fecha de publicación asignada
        if self.estado_publicacion_esta_publicado and self.fecha_publicacion is None:
            # Asigna la fecha/hora actual como fecha de publicación
            self.fecha_publicacion = timezone.now()
        else:
            # Si no está publicado o ya tiene fecha, elimina la fecha de publicación
            self.fecha_publicacion = None
            
        # Llama al método save() de la clase padre para guardar los cambios
        super().save(*args, **kwargs)