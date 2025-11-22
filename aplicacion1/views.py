from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from CONTEO_PERSONAS.detector_personas import ConteoPersonas, procesar_video
from .models import Laboratorio, Reporte, Captura
import json
import base64
from django.core.files.base import ContentFile
from datetime import datetime

contador_global = None

def index(request):
    return render(request, 'aplicacion1/index.html')

def generar_frames():
    global contador_global
    if contador_global is None:
        contador_global = ConteoPersonas()
        
    for resultado in procesar_video(contador_global):
        yield f"data: {json.dumps(resultado)}\n\n"

def video_feed(request):
    return StreamingHttpResponse(
        generar_frames(),
        content_type='text/event-stream'
    )

def iniciar(request):
    global contador_global
    if contador_global is None:
        contador_global = ConteoPersonas()
    elif not contador_global.esta_ejecutando():
        contador_global.running = True
    return JsonResponse({'status': 'iniciado'})

def detener(request):
    global contador_global
    if contador_global and contador_global.esta_ejecutando():
        contador_global.detener()
        return JsonResponse({'status': 'detenido'})
    return JsonResponse({'status': 'no está ejecutándose'})

def obtener_estadisticas(request):
    global contador_global
    if contador_global:
        return JsonResponse({
            'contador': contador_global.get_conteo(),
            'historico': contador_global.get_historico()[-10:]  # últimos 10 registros
        })
    return JsonResponse({'error': 'No hay sesión activa'})


def crear_laboratorio(nombre):
    try:
        laboratorio, created = Laboratorio.objects.get_or_create(nombre=nombre)
    except Exception as e:
        print(f"Error al crear el laboratorio: {e}")
        return None


@csrf_exempt
def guardar_reporte(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Obtener o crear laboratorio
            nombre_lab = data.get('laboratorio', 'Laboratorio Principal')
            laboratorio, _ = Laboratorio.objects.get_or_create(nombre=nombre_lab)
            
            # Obtener contador actual
            global contador_global
            numero_personas = data.get('numero_personas', 0)
            if contador_global:
                numero_personas = contador_global.get_conteo()
            
            # Crear reporte
            reporte = Reporte.objects.create(
                laboratorio=laboratorio,
                numero_personas=numero_personas,
                observaciones=data.get('observaciones', '')
            )
            
            # Guardar capturas si existen
            capturas_data = data.get('capturas', [])
            capturas_guardadas = 0
            
            for captura_info in capturas_data:
                try:
                    imagen_base64 = captura_info.get('imagen', '')
                    personas = captura_info.get('personas', 0)
                    
                    # Crear captura
                    captura = Captura.objects.create(
                        reporte=reporte,
                        imagen_base64=imagen_base64,
                        numero_personas=personas
                    )
                    capturas_guardadas += 1
                    
                except Exception as e:
                    print(f"Error al guardar captura: {e}")
                    continue
            
            return JsonResponse({
                'status': 'success',
                'mensaje': 'Reporte guardado correctamente',
                'reporte_id': reporte.id,
                'capturas_guardadas': capturas_guardadas
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'mensaje': f'Error al guardar reporte: {str(e)}'
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'mensaje': 'Método no permitido'
    }, status=405)