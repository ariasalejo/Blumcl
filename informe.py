"""Genera el informe HTML y lo copia a Download."""
import json
import shutil
from pathlib import Path

from blumcl.reports.html import generar

snaps = sorted(Path("data/snapshots").glob("*.json"))
if not snaps:
    print("❌ Aún no hay snapshots: corre blumcl → opción 1.")
else:
    out = generar(json.loads(snaps[-1].read_text()))
    copia = Path.home() / "storage" / "shared" / "Download" / "informe.html"
    shutil.copy(out, copia)
    print("✅ Informe:", out)
    print("📱 Copiado a Download.")
