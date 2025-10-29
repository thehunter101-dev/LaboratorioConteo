# Conteo de laboratorio con Django + OpenCV

Descripción
-----------
Proyecto de ejemplo que integra Django con OpenCV para mostrar un stream de vídeo, detectar y contar personas, y permitir capturas. Incluye una interfaz web minimalista y responsive. Este README explica cómo configurar, ejecutar y probar el proyecto en desarrollo (Windows / PowerShell) y los detalles relevantes sobre archivos estáticos y frontend.

Requisitos
---------
- Python 3.10+ (se recomienda 3.11+)
- pip
- virtualenv (opcional pero recomendado)
- Dependencias listadas en `requirements.txt`

Estructura relevante
--------------------
ConteoPersonasLaboratorio/
	├─ CONTEO_PERSONAS/        # settings, urls, wsgi, etc.
	├─ aplicacion1/            # app principal (vistas, templates, static)
	│   ├─ templates/aplicacion1/index.html
	│   └─ static/aplicacion1/css/style.css
	├─ db.sqlite3
	└─ manage.py

Instalación (desarrollo)
------------------------
Abre PowerShell y ejecuta:

```powershell
# crear y activar entorno virtual (opcional)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# instalar dependencias
pip install -r requirements.txt
```

Configuración de archivos estáticos
----------------------------------
El proyecto ya incluye una configuración básica en `CONTEO_PERSONAS/settings.py`:

- `STATIC_URL = '/static/'`
- `STATICFILES_DIRS = [ BASE_DIR / 'aplicacion1' / 'static' ]` — aquí están los CSS/JS de la app durante desarrollo
- `STATIC_ROOT = BASE_DIR / 'staticfiles'` — destino para `collectstatic` en producción

En desarrollo Django sirve los archivos estáticos automáticamente cuando `DEBUG = True`. Además en `CONTEO_PERSONAS/urls.py` se añadió la ruta para servir estáticos:

```py
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
		urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

Frontend / Cambios realizados
----------------------------
- Separé el CSS en `aplicacion1/static/aplicacion1/css/style.css` y el HTML ahora carga el CSS con la etiqueta `{% load static %}` y
	`<link href="{% static 'aplicacion1/css/style.css' %}" rel="stylesheet">`.
- El layout se rediseñó a un estilo más minimalista: área de vídeo a la izquierda y barra lateral a la derecha (conteo, histórico, capturas), responsive usando CSS Grid/Flexbox.

Endpoints útiles (mapeados en `CONTEO_PERSONAS/urls.py`)
-----------------------------------------------------
- `/` — vista principal que renderiza `index.html`
- `/iniciar/` — inicia el proceso de conteo (llamada desde el frontend)
- `/detener/` — detiene el proceso
- `/video_feed/` — EventSource / streaming de frames en base64
- `/estadisticas/` — devuelve historiales y estadísticas (JSON)

Ejecutar la app (desarrollo)
----------------------------
En PowerShell (entorno activado):

```powershell
# aplicar migraciones (si corresponde)
python manage.py migrate

# ejecutar servidor de desarrollo
python manage.py runserver
```

Prueba rápida del frontend
-------------------------
1. Abre el navegador en `http://127.0.0.1:8000/`.
2. Inspecciona (F12) la pestaña Network y verifica que `aplicacion1/css/style.css` se carga sin 404.
3. Usa los botones `Iniciar` / `Detener` para probar las llamadas a `/iniciar/` y `/detener/`.

Producción
----------
Antes de desplegar en producción:

```powershell
# recolectar archivos estáticos en STATIC_ROOT
python manage.py collectstatic --noinput
```

Notas / Troubleshooting
-----------------------
- Si el CSS no se carga en desarrollo: verifica que `DEBUG = True` y que `STATICFILES_DIRS` apunta a `aplicacion1/static`.
- Si ves 404 en `/static/...` bajo DEBUG: reinicia el servidor de desarrollo.
- Si usas un proxy o servidor (nginx, apache) en producción, sirve `STATIC_ROOT` desde el servidor web.
- En Windows + PowerShell, si tienes problemas al activar el venv por políticas de ejecución, puedes usar:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Mejoras sugeridas / próximos pasos
---------------------------------
- Agregar tests automatizados para endpoints JSON (`/estadisticas/`).
- Incluir un archivo `requirements-dev.txt` con herramientas de linting.
- Añadir instrucciones de despliegue con Gunicorn + Nginx (si se planea producción).

Contacto
-------
Si quieres que adapte el diseño (colores, tipografía, posiciones) o que añada un tema oscuro, dime qué estilo prefieres y lo implemento.

Resumen de cambios hechos en el repo
-----------------------------------
- `aplicacion1/static/aplicacion1/css/style.css` (nuevo archivo CSS)
- `aplicacion1/templates/aplicacion1/index.html` (actualizado para cargar CSS y nuevo layout)
- `CONTEO_PERSONAS/settings.py` (añadido STATIC_ROOT y STATICFILES_DIRS)
- `CONTEO_PERSONAS/urls.py` (añadidos imports y configuración estáticos en DEBUG)

# Conteo de laboratorio con Django + Opencv
