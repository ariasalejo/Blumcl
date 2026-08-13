import tempfile
import unittest
from pathlib import Path

from blumcl.scanners.storage.scanner import (
    _confianza_archivo_grande,
    _normalizar_zonas,
    _esta_protegida,
    generar_evidencias_archivos_grandes,
    espacio,
)


class TestStorageScanner(unittest.TestCase):

    def test_espacio_contiene_metricas(self):
        resultado = espacio()

        self.assertIn(
            "total_gb",
            resultado,
        )

        self.assertIn(
            "usado_gb",
            resultado,
        )

        self.assertIn(
            "libre_gb",
            resultado,
        )

        self.assertGreater(
            resultado["total_gb"],
            0,
        )

    def test_confianza_archivo_muy_grande(self):
        confianza = _confianza_archivo_grande(
            10 * 1_000_000_000
        )

        self.assertEqual(
            confianza,
            0.97,
        )

    def test_confianza_archivo_menor(self):
        confianza = _confianza_archivo_grande(
            100 * 1_000_000
        )

        self.assertEqual(
            confianza,
            0.70,
        )

    def test_normalizar_zonas(self):
        with tempfile.TemporaryDirectory() as directory:
            zona = Path(directory)

            resultado = _normalizar_zonas(
                [str(zona)]
            )

            self.assertIn(
                zona.resolve(),
                resultado,
            )

    def test_ruta_protegida(self):
        with tempfile.TemporaryDirectory() as directory:
            zona = Path(directory)

            zonas = _normalizar_zonas(
                [str(zona)]
            )

            archivo = zona / "importante.txt"

            self.assertTrue(
                _esta_protegida(
                    archivo,
                    zonas,
                )
            )

    def test_ruta_no_protegida(self):
        with tempfile.TemporaryDirectory() as directory:
            zona = Path(directory) / "protegida"

            zona.mkdir()

            zonas = _normalizar_zonas(
                [str(zona)]
            )

            archivo = (
                Path(directory)
                / "normal.txt"
            )

            self.assertFalse(
                _esta_protegida(
                    archivo,
                    zonas,
                )
            )

    def test_generar_evidencia(self):
        with tempfile.TemporaryDirectory() as directory:
            archivo = (
                Path(directory)
                / "archivo-grande.zip"
            )

            archivo.write_bytes(
                b"BLUMCL" * 100
            )

            hallazgos = [
                {
                    "mb": 0.0006,
                    "ruta": str(archivo),
                }
            ]

            evidencias = (
                generar_evidencias_archivos_grandes(
                    hallazgos,
                    sequence_start=50,
                    snapshot_id="BLUMCL-S-TEST",
                )
            )

            self.assertEqual(
                len(evidencias),
                1,
            )

            evidencia = evidencias[0]

            self.assertEqual(
                evidencia.evidence_id,
                "BLUMCL-E-000050",
            )

            self.assertEqual(
                evidencia.snapshot_id,
                "BLUMCL-S-TEST",
            )

            self.assertEqual(
                evidencia.path,
                str(archivo),
            )

            self.assertTrue(
                evidencia.has_reasons()
            )

            self.assertEqual(
                evidencia.action.value,
                "none",
            )

            self.assertIsNotNone(
                evidencia.recommendation
            )

    def test_generar_evidencia_no_modifica_archivo(self):
        with tempfile.TemporaryDirectory() as directory:
            archivo = (
                Path(directory)
                / "protegido.txt"
            )

            contenido = (
                "BLUMCL NO MODIFICAR"
            )

            archivo.write_text(
                contenido,
                encoding="utf-8",
            )

            hallazgos = [
                {
                    "mb": 0.01,
                    "ruta": str(archivo),
                }
            ]

            generar_evidencias_archivos_grandes(
                hallazgos,
                sequence_start=1,
            )

            self.assertEqual(
                archivo.read_text(
                    encoding="utf-8"
                ),
                contenido,
            )


if __name__ == "__main__":
    unittest.main()
