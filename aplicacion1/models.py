from django.db import models
from django.utils import timezone


class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Reporte(models.Model):
    laboratorio = models.ForeignKey(
        Laboratorio, on_delete=models.CASCADE, related_name="reportes"
    )
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    numero_personas = models.PositiveIntegerField()
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reporte {self.fecha} {self.hora} - {self.laboratorio.nombre}"


class Captura(models.Model):
    reporte = models.ForeignKey(
        Reporte, on_delete=models.CASCADE, related_name="capturas"
    )
    imagen = models.ImageField(upload_to='capturas/%Y/%m/%d/', blank=True, null=True)
    imagen_base64 = models.TextField(blank=True, null=True)
    numero_personas = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Captura {self.timestamp} - {self.numero_personas} personas"
