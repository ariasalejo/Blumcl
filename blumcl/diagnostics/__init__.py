"""
BLUMCL · Diagnostic Engine

Capa de orquestación para los scanners de BLUMCL.

Responsabilidad:
    Coordinar observación → evidencia → resultado.

Importante:
    Este módulo NO modifica el sistema.
    Este módulo NO ejecuta acciones destructivas.
    Este módulo NO permite que la IA actúe sobre el sistema.
"""

from .diagnostic import DiagnosticEngine, DiagnosticResult

__all__ = [
    "DiagnosticEngine",
    "DiagnosticResult",
]
