from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio_regular = models.DecimalField(max_digits=10, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    variantes = models.TextField(blank=True)
    url_imagen = models.URLField(blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre