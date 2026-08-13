"""Blumcl · IA local privada.

Puente entre Blumcl y el modelo local (llama.cpp / Qwen3).
Regla de oro: la IA interpreta y recomienda. NUNCA actúa.
"""

import shutil
import subprocess
from pathlib import Path

MODELO_POR_DEFECTO = Path.home() / "qwen3.gguf"


class IALocal:
    """Cliente del modelo que vive en tu celular."""

    def __init__(self, modelo=MODELO_POR_DEFECTO, hilos=4, contexto=2048):
        self.modelo = Path(modelo)
        self.hilos = hilos
        self.contexto = contexto

    def disponible(self):
        """True si existe llama-cli y el modelo está en disco."""
        return shutil.which("llama-cli") is not None and self.modelo.exists()

    def preguntar(self, pregunta, max_tokens=400, timeout=240):
        """Una pregunta → una respuesta. Sin internet."""
        if not self.disponible():
            return "[Blumcl] IA no disponible (falta llama-cli o el modelo)."
        cmd = [
            "llama-cli",
            "-m", str(self.modelo),
            "-cnv",
            "--color", "on",
            "-t", "4",
            "-c", "4096",
            "--temp", "0.7",
            "--repeat-penalty", "1.1",
            "-p", "Eres Blumcl-IA, analista local de un teléfono Android. Responde SIEMPRE en español, breve y claro. Filosofía: observar antes de actuar, nunca ordenar borrar sin confirmación humana.",
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return r.stdout.strip()
        except subprocess.TimeoutExpired:
            return "[Blumcl] La IA tardó demasiado en responder."

    def interpretar_evidencia(self, evidencia_texto):
        """Flujo de tu arquitectura: EVIDENCIA → IA → INTERPRETACIÓN."""
        prompt = (
            "Eres Blumcl-IA, analista local de un teléfono Android. "
            "Responde en español, breve y claro. No inventes capacidades. "
            "Lee la evidencia y da: 1) diagnóstico, 2) tres recomendaciones. "
            "NUNCA ordenes borrar archivos sin confirmación humana.\n\n"
            f"EVIDENCIA:\n{evidencia_texto}\n\nANÁLISIS:"
        )
        return self.preguntar(prompt, max_tokens=400)
