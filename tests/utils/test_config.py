"""Pruebas de la configuración segura de Blumcl."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from blumcl.utils import config


class TestConfiguracion(unittest.TestCase):
    """Verifica los valores de protección de Blumcl."""

    def test_defaults_contienen_zonas_protegidas(self):
        """Los valores predeterminados deben proteger rutas críticas."""
        self.assertIn(".ssh", config.DEFAULTS["zonas_intocables"])
        self.assertIn(".termux", config.DEFAULTS["zonas_intocables"])
        self.assertIn(".gnupg", config.DEFAULTS["zonas_intocables"])

    def test_defaults_contienen_extensiones_criticas(self):
        """Las extensiones sensibles deben estar protegidas."""
        self.assertIn(".key", config.DEFAULTS["extensiones_criticas"])
        self.assertIn(".pem", config.DEFAULTS["extensiones_criticas"])
        self.assertIn(".gpg", config.DEFAULTS["extensiones_criticas"])

    def test_tamano_grande_es_valido(self):
        """Debe existir un umbral razonable para archivos grandes."""
        self.assertGreater(config.DEFAULTS["tamano_grande_mb"], 0)

    def test_cargar_configuracion_valida(self):
        """Una configuración válida debe poder cargarse."""
        datos = {
            "zonas_intocables": [".ssh"],
            "extensiones_criticas": [".key"],
            "tamano_grande_mb": 50,
        }

        with TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "proteccion.json"
            ruta.write_text(
                json.dumps(datos),
                encoding="utf-8",
            )

            with patch.object(config, "RUTA", ruta):
                resultado = config.cargar()

        self.assertEqual(resultado["zonas_intocables"], [".ssh"])
        self.assertEqual(resultado["tamano_grande_mb"], 50)


if __name__ == "__main__":
    unittest.main()
