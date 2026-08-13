"""
Pruebas del BLUMCL CPU Scanner.
"""

import unittest

from blumcl.scanners.cpu.scanner import CPUInfo, scan


class TestCPUInfo(unittest.TestCase):

    def test_crear_cpu_info_valido(self):
        info = CPUInfo(
            architecture="aarch64",
            processor="test-cpu",
            logical_cpus=8,
        )

        self.assertEqual(info.architecture, "aarch64")
        self.assertEqual(info.processor, "test-cpu")
        self.assertEqual(info.logical_cpus, 8)

    def test_to_dict(self):
        info = CPUInfo(
            architecture="aarch64",
            processor="test-cpu",
            logical_cpus=8,
        )

        self.assertEqual(
            info.to_dict(),
            {
                "architecture": "aarch64",
                "processor": "test-cpu",
                "logical_cpus": 8,
            },
        )

    def test_rechaza_arquitectura_vacia(self):
        with self.assertRaises(ValueError):
            CPUInfo("", "test-cpu", 8)

    def test_rechaza_processor_vacio(self):
        with self.assertRaises(ValueError):
            CPUInfo("aarch64", "", 8)

    def test_rechaza_cpus_invalidas(self):
        with self.assertRaises(ValueError):
            CPUInfo("aarch64", "test-cpu", 0)


class TestCPUScanner(unittest.TestCase):

    def test_scan_devuelve_cpu_info(self):
        resultado = scan()
        self.assertIsInstance(resultado, CPUInfo)

    def test_scan_tiene_arquitectura(self):
        resultado = scan()
        self.assertTrue(resultado.architecture.strip())

    def test_scan_tiene_processor(self):
        resultado = scan()
        self.assertTrue(resultado.processor.strip())

    def test_scan_tiene_cpus_validas(self):
        resultado = scan()
        self.assertGreater(resultado.logical_cpus, 0)

    def test_scan_to_dict(self):
        datos = scan().to_dict()

        self.assertIsInstance(datos, dict)
        self.assertIn("architecture", datos)
        self.assertIn("processor", datos)
        self.assertIn("logical_cpus", datos)


if __name__ == "__main__":
    unittest.main()
