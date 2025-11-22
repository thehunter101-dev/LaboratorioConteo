# Sistema de Conteo de Personas - Instrucciones

## Nuevas Funcionalidades Implementadas

### 1. Botón "Guardar Reporte"
- **Ubicación**: Panel de controles junto a los botones Iniciar, Detener y Capturar
- **Función**: Guarda en la base de datos el conteo actual y todas las capturas realizadas

### 2. Modelos de Base de Datos Actualizados

#### Modelo Reporte
- `laboratorio`: Referencia al laboratorio
- `fecha`: Fecha automática del reporte
- `hora`: Hora automática del reporte
- `numero_personas`: Cantidad de personas detectadas
- `observaciones`: Campo de texto para notas adicionales
- `created_at`: Timestamp de creación

#### Modelo Captura
- `reporte`: Referencia al reporte asociado
- `imagen`: Campo para guardar imagen física (opcional)
- `imagen_base64`: Almacenamiento de imagen en formato base64
- `numero_personas`: Personas detectadas en la captura
- `timestamp`: Momento de la captura

### 3. Mejoras de Diseño

#### Visuales
- **Gradiente de fondo** moderno en toda la aplicación
- **Contador de personas** con gradiente morado y efecto de sombra
- **Tarjetas** con efectos hover y transiciones suaves
- **Botones** con sombras y animaciones al hacer clic
- **Alertas** con animación de entrada y colores mejorados
- **Historial** con efecto de desplazamiento al pasar el cursor

#### Responsive
- Diseño adaptable para móviles, tablets y escritorio
- Controles que se apilan verticalmente en pantallas pequeñas

## Cómo Usar

### 1. Iniciar el Sistema
```bash
python manage.py runserver
```

### 2. Capturar Imágenes
1. Clic en **Iniciar** para comenzar el conteo
2. Clic en **Capturar** para tomar una foto del momento actual
3. Las capturas aparecerán en el panel derecho con el conteo de personas

### 3. Guardar Reporte
1. Después de realizar varias capturas
2. Clic en **Guardar Reporte** (botón amarillo)
3. El sistema guardará:
   - El conteo actual de personas
   - Todas las capturas realizadas
   - Fecha y hora automáticas
4. Opción de limpiar las capturas después de guardar

### 4. Ver Reportes Guardados
Los reportes se pueden consultar desde:
- Panel de administración de Django: `/admin/`
- Usuario: crear un superusuario con `python manage.py createsuperuser`

## Archivos Modificados

1. **models.py**: Nuevos modelos Reporte y Captura con campos de imagen
2. **views.py**: Vista `guardar_reporte` para procesar y guardar datos
3. **urls.py**: Configuración de rutas para archivos media
4. **settings.py**: Configuración MEDIA_URL y MEDIA_ROOT
5. **index.html**: Botón de guardar reporte con JavaScript funcional
6. **style.css**: Mejoras visuales completas
7. **requirements.txt**: Agregado Pillow para procesamiento de imágenes

## Características Técnicas

### Backend
- Manejo de imágenes base64 para almacenamiento
- Decorador `@csrf_exempt` para peticiones POST
- Relaciones ForeignKey entre modelos
- Auto-generación de fechas y horas

### Frontend
- jQuery para manejo de eventos
- AJAX para comunicación asíncrona
- Animaciones CSS para mejor UX
- Almacenamiento temporal de capturas en el DOM

### Base de Datos
- SQLite por defecto
- Migraciones aplicadas automáticamente
- Soporte para ImageField (requiere Pillow)

## Dependencias Nuevas

```
Pillow==11.0.0  # Para procesamiento de imágenes
```

Instalar con:
```bash
pip install -r requirements.txt
```

## Estructura de Carpetas

```
LaboratorioConteo-main/
├── media/                  # Carpeta para archivos subidos
│   └── capturas/          # Imágenes de capturas organizadas por fecha
├── aplicacion1/
│   ├── models.py          # Modelos actualizados
│   ├── views.py           # Vistas con guardar_reporte
│   └── templates/
│       └── aplicacion1/
│           └── index.html # Template mejorado
└── CONTEO_PERSONAS/
    ├── settings.py        # Configuración de MEDIA
    └── urls.py           # Rutas para archivos media
```

## Notas Importantes

1. Las capturas se guardan en formato base64 en la base de datos
2. El campo `imagen` del modelo Captura permite guardar archivos físicos (opcional)
3. Los reportes están ordenados por fecha descendente
4. El sistema pregunta si desea limpiar las capturas después de guardar
5. Todas las operaciones son no bloqueantes con feedback visual

## Próximas Mejoras Sugeridas

- [ ] Panel de visualización de reportes históricos
- [ ] Exportación de reportes a PDF
- [ ] Gráficos estadísticos del historial
- [ ] Filtros por fecha y laboratorio
- [ ] Notificaciones por correo de reportes
