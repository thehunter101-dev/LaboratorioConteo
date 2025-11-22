from django.contrib import admin
from .models import Laboratorio, Reporte, Captura


@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'laboratorio', 'fecha', 'hora', 'numero_personas', 'created_at')
    list_filter = ('fecha', 'laboratorio')
    search_fields = ('laboratorio__nombre', 'observaciones')
    date_hierarchy = 'fecha'
    readonly_fields = ('created_at',)


@admin.register(Captura)
class CapturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporte', 'numero_personas', 'timestamp', 'tiene_imagen')
    list_filter = ('timestamp', 'reporte__laboratorio')
    search_fields = ('reporte__observaciones',)
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)
    
    def tiene_imagen(self, obj):
        return bool(obj.imagen_base64 or obj.imagen)
    tiene_imagen.boolean = True
    tiene_imagen.short_description = 'Tiene Imagen'
