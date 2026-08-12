#!/usr/bin/env python
"""Blumcl · Terminal de Mando v0.3.0."""

import json

from blumcl.ai import IALocal
from blumcl.scanners.storage import scanner
from blumcl.utils.config import cargar

VERSION = "0.3.0"


def cabecera():
    try:
        e = scanner.espacio()
        disco = f"💾 {e['libre_gb']} GB libres de {e['total_gb']} GB"
    except Exception:
        disco = "💾 disco: n/d"
    print(f"""
╔════════════════════════════════════════════╗
║          🚀  B L U M C L  v{VERSION}           ║
║  Observar · Analizar · Confirmar · Actuar  ║
╠════════════════════════════════════════════╣
║  {disco}{' ' * max(0, 42 - len(disco))}║
╚════════════════════════════════════════════╝""")


MENU = """
  [1] 🔬 Escanear almacenamiento
  [2] 📊 Generar informe HTML
  [3] ⏳ Comparar snapshots (qué cambió)
  [4] 🗂️  Historial de snapshots
  [5] 🤖 Preguntar a la IA
  [6] 🩺 Autodiagnóstico
  [7] 🧹 Limpieza controlada (dry-run)
  [8] 🛡️  Ver zonas protegidas
  [9] ⚙️  Configuración
  [0] 👋 Salir
"""


def main():
    ia = IALocal()
    while True:
        cabecera()
        print(MENU)
        op = input("→ ").strip()

        if op == "1":
            print("\n🔬 Observando (sin modificar)...")
            datos = scanner.analizar()
            e = datos["espacio"]
            print(f"\n💾 {e['usado_gb']} GB usados de {e['total_gb']} GB")
            print("\n🐘 Archivos más grandes:")
            for a in datos["archivos_grandes"]:
                print(f"   {a['mb']:>8} MB  {a['ruta']}")
            snap = scanner.guardar_snapshot(datos)
            print(f"\n📊 Snapshot: {snap.name}")
            if input("🤖 ¿Análisis de la IA? (s/n): ").strip().lower() == "s":
                print(ia.interpretar_evidencia(
                    json.dumps(datos, ensure_ascii=False)))
        elif op == "5":
            q = input("Tu pregunta: ").strip()
            if q:
                print("\n🤖 Pensando...\n")
                print(ia.preguntar(q, 300))
        elif op == "6":
            for a in scanner.autodiagnostico():
                print("⚠️ ", a)
        elif op == "8":
            cfg = cargar()
            print("\n🛡️  Zonas intocables:")
            for z in cfg["zonas_intocables"]:
                print("   🔒", z)
        elif op == "9":
            print("\n⚙️  Configuración actual:")
            print(json.dumps(cargar(), ensure_ascii=False, indent=2))
        elif op == "0":
            print("👋 Hasta pronto, Blumix.")
            break
        elif op == "2":
            import shutil
            from pathlib import Path
            from blumcl.reports.html import generar
            snaps = sorted(scanner.SNAPSHOTS.glob("*.json"))
            if not snaps:
                print("❌ No hay snapshots: usa la opción 1.")
            else:
                out = generar(json.loads(snaps[-1].read_text()))
                print("📄 Reporte generado:", out)
                if input("📥 ¿Descargar tu reporte? (y/n): ").strip().lower() == "y":
                    copia = Path.home() / "storage" / "shared" / "Download" / "informe.html"
                    shutil.copy(out, copia)
                    print("✅ En Download → Archivos → Download → informe.html → Chrome.")
        elif op in ("3", "4", "7"):
            print("🚧 En construcción — llega en el siguiente bloque.")
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    main()
