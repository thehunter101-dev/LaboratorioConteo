import cv2
from datetime import datetime
import base64

class ConteoPersonas:
    def __init__(self):
        # Cargar los clasificadores en cascada para rostros
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.personas_count = 0
        self.conteo_historico = []
        self.running = True
        self.min_face_size = (60, 60)  # Tamaño mínimo para detectar un rostro

    def procesar_frame(self, frame):
        if frame is None:
            return None

        # Redimensionar el frame para mejor rendimiento y visualización web
        height, width = frame.shape[:2]
        frame = cv2.resize(frame, (960, 540))  # Resolución más pequeña (HD/2)

        # Preparar imagen para detección
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)  # Mejorar contraste
        detecciones = []

        # Detectar rostros con parámetros optimizados
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=self.min_face_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Procesar detecciones válidas
        for (x, y, w, h) in faces:
            # Verificar proporción del rostro
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2:
                detecciones.append([x, y, w, h])
                # Dibujar rectángulo y etiqueta
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, 'Rostro', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Actualizar conteo y registro histórico
        self.personas_count = len(detecciones)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conteo_historico.append((timestamp, self.personas_count))

        # Mostrar conteo con mejor diseño
        cv2.rectangle(frame, (10, 10), (300, 70), (0, 0, 0), -1)
        cv2.putText(frame, f'Personas detectadas: {self.personas_count}', 
                   (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Convertir frame a formato base64 para transmisión web
        _, buffer = cv2.imencode('.jpg', frame)
        frame_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            'frame': frame_b64,
            'count': self.personas_count,
            'timestamp': timestamp
        }

    def get_conteo(self):
        return self.personas_count

    def get_historico(self):
        return self.conteo_historico

    def detener(self):
        self.running = False

    def esta_ejecutando(self):
        return self.running

def procesar_video(contador):
    cap = cv2.VideoCapture(0)
    
    # Configurar la cámara para mejor calidad
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    while contador.esta_ejecutando():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Procesar el frame
        resultado = contador.procesar_frame(frame)
        if resultado is None:
            break
            
        yield resultado
        
    cap.release()
