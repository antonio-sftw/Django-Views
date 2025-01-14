from django.core.exceptions import ValidationError # type: ignore

# Validador de palabras bloqueadas

BLOCKED_WORDS = ['menso', 'caracoles', 'repapanos', 'goserias fuertes']

def validate_blocked_words(value):
    string = value.lower() # Convertir a minúsculas
    palabras_unicas = set(string.split()) # Convertir a set para eliminar duplicados
    blocked_words = set(BLOCKED_WORDS)
    invalid_words = palabras_unicas & blocked_words # Intersección de conjuntos, almacena las palabras que coinciden
    if len(invalid_words) > 0:
        errores = []
        for palabra in invalid_words:
            errores.append("{} no está permitido".format(palabra))
        raise ValidationError(errores)
    # Si no hay palabras bloqueadas, retorna el valor original
    return value