"""Prueba básica del puente de IA."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

from blumcl.ai import IALocal

ia = IALocal()
assert ia.disponible(), "La IA debería estar disponible"
print("✅ test_ai: el puente funciona")
