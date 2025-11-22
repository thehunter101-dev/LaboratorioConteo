from django.test import TestCase, Client
from django.urls import reverse
from aplicacion1.models import Laboratorio, Reporte, Captura


class UrlTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_Iniciar_camera(self):
        url = reverse("iniciar")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "iniciado"})

    def test_Reporte(self):
        url = reverse('reporte')
        data = {
            "laboratorio": "Laboratorio Test",
            "numero_personas": 5,
            "observaciones": "Test reporte",
            "capturas": [
                {
                    "imagen": "data:image/jpeg;base64,test123",
                    "personas": 5
                }
            ]
        }
        response = self.client.post(
            url,
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        
        self.assertIn("status", json_data)
        self.assertEqual(json_data["status"], "success")
        self.assertIn("capturas_guardadas", json_data)
        self.assertEqual(json_data["capturas_guardadas"], 1)

    def test_Reporte_faltan_parametros(self):
        url = reverse('reporte')
        # Enviar datos incompletos (sin capturas pero con estructura válida)
        data = {
            "laboratorio": "Laboratorio Test",
            "numero_personas": 3,
            "capturas": []
        }
        response = self.client.post(
            url,
            data=data,
            content_type='application/json'
        )

        # Debe devolver éxito aunque no haya capturas
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        
        self.assertIn("status", json_data)
        self.assertEqual(json_data["status"], "success")
        self.assertEqual(json_data["capturas_guardadas"], 0)

    def test_integracion_completa_camara_conteo_reporte(self):

        url_iniciar = reverse("iniciar")
        response_iniciar = self.client.get(url_iniciar)
        self.assertEqual(response_iniciar.status_code, 200)
        self.assertJSONEqual(response_iniciar.content, {"status": "iniciado"})
        
        url_estadisticas = reverse("estadisticas")
        response_estadisticas = self.client.get(url_estadisticas)
        self.assertEqual(response_estadisticas.status_code, 200)
        estadisticas_data = response_estadisticas.json()
        self.assertIn("contador", estadisticas_data)
        
        conteo_actual = estadisticas_data.get("contador", 0)
        
        capturas_simuladas = [
            {
                "imagen": "data:image/jpeg;base64,/9j/4AAQSkZJRg==",
                "personas": 3
            },
            {
                "imagen": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAA",
                "personas": 5
            },
            {
                "imagen": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA",
                "personas": 4
            }
        ]
        
        url_reporte = reverse('reporte')
        numero_personas_esperado = 5  # Valor por defecto para pruebas
        data_reporte = {
            "laboratorio": "Laboratorio Integración",
            "numero_personas": numero_personas_esperado,
            "observaciones": "Reporte de prueba de integración completa",
            "capturas": capturas_simuladas
        }
        
        response_reporte = self.client.post(
            url_reporte,
            data=data_reporte,
            content_type='application/json'
        )
        
        self.assertEqual(response_reporte.status_code, 200)
        reporte_data = response_reporte.json()
        
        self.assertEqual(reporte_data["status"], "success")
        self.assertEqual(reporte_data["capturas_guardadas"], 3)
        self.assertIn("reporte_id", reporte_data)
        
        reporte_id = reporte_data["reporte_id"]
        reporte_guardado = Reporte.objects.get(id=reporte_id)
        
        self.assertEqual(reporte_guardado.laboratorio.nombre, "Laboratorio Integración")
        self.assertGreaterEqual(reporte_guardado.numero_personas, 0)
        self.assertEqual(reporte_guardado.observaciones, "Reporte de prueba de integración completa")
        
        capturas_guardadas = Captura.objects.filter(reporte=reporte_guardado)
        self.assertEqual(capturas_guardadas.count(), 3)
        
        for idx, captura in enumerate(capturas_guardadas.order_by('id')):
            self.assertIsNotNone(captura.imagen_base64)
            self.assertGreater(len(captura.imagen_base64), 0)
            self.assertEqual(captura.numero_personas, capturas_simuladas[idx]["personas"])
            self.assertIsNotNone(captura.timestamp)
        
        url_detener = reverse("detener")
        response_detener = self.client.get(url_detener)
        self.assertEqual(response_detener.status_code, 200)
        detener_data = response_detener.json()
        self.assertIn("status", detener_data)

