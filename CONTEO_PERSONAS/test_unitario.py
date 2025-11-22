import unittest
import numpy as np
from unittest.mock import MagicMock
from .detector_personas import ConteoPersonas


class TestConteoPersonas(unittest.TestCase):

    def test_constructor(self):
        cp = ConteoPersonas()
        self.assertEqual(cp.personas_count, 0)
        self.assertTrue(cp.running)
        self.assertEqual(cp.conteo_historico, [])

    def test_procesar_frame_none(self):
        cp = ConteoPersonas()
        resultado = cp.procesar_frame(None)
        self.assertIsNone(resultado)

    def test_procesar_frame_sin_rostros(self):
        cp = ConteoPersonas()

        # Crear un frame negro (sin rostros)
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Mock: detectMultiScale no detecta nada
        mock_cascade = MagicMock()
        mock_cascade.detectMultiScale = MagicMock(return_value=[])
        cp.face_cascade = mock_cascade

        resultado = cp.procesar_frame(frame)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["count"], 0)
        self.assertEqual(cp.get_conteo(), 0)
        self.assertEqual(len(cp.get_historico()), 1)

    def test_procesar_frame_con_rostros(self):
        cp = ConteoPersonas()

        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Mock: detecta 2 rostros
        mock_cascade = MagicMock()
        mock_cascade.detectMultiScale = MagicMock(
            return_value=[(10, 10, 80, 80), (200, 10, 85, 85)]
        )
        cp.face_cascade = mock_cascade

        resultado = cp.procesar_frame(frame)

        self.assertEqual(resultado["count"], 2)
        self.assertEqual(cp.get_conteo(), 2)
        self.assertEqual(len(cp.get_historico()), 1)

    def test_get_conteo(self):
        cp = ConteoPersonas()
        cp.personas_count = 5
        self.assertEqual(cp.get_conteo(), 5)

    def test_get_historico(self):
        cp = ConteoPersonas()
        cp.conteo_historico.append(("fecha", 3))
        self.assertEqual(cp.get_historico(), [("fecha", 3)])

    def test_detener(self):
        cp = ConteoPersonas()
        cp.detener()
        self.assertFalse(cp.esta_ejecutando())


if __name__ == "__main__":
    unittest.main()
