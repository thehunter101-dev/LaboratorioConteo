from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from CONTEO_PERSONAS.detector_personas import ConteoPersonas, procesar_video
import json

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
