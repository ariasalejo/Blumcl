"""Pruebas del puente de IA local de Blumcl."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

from blumcl.ai import IALocal


class TestIALocal(unittest.TestCase):
    """Pruebas básicas de la IA local."""

    def setUp(self):
        self.ia = IALocal()

    def test_ia_disponible(self):
        """La IA local debe estar disponible."""
        self.assertTrue(
            self.ia.disponible(),
            "La IA local debería estar disponible",
        )


if __name__ == "__main__":
    unittest.main()
