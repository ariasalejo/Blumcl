#!/usr/bin/env python
"""Blumcl · aplicación principal (menú por números)."""

import json

from blumcl.ai import IALocal
from blumcl.scanners.storage import scanner


def main():
    ia = IALocal()
    while True:
        print("\n🚀 BLUMCL · menú")
        print(" 1) Estado de la IA local")
        print(" 2) Preguntar a la IA")
        print(" 3) Escanear almacenamiento (observar sin modificar)")
        print(" 4) Autodiagnóstico")
        print(" 5) Salir")
        op = input("→ ").strip()

        if op == "1":
            print("✅ IA lista." if ia.disponible()
                  else "❌ Falta llama-cli o el modelo.")
        elif op == "2":
            q = input("Tu pregunta: ").strip()
            if q:
                print("\n🤖 Pensando...\n")
                print(ia.preguntar(q, 300))
        elif op == "3":
            print("\n🔬 Observando (sin modificar)...")
            datos = scanner.analizar()
            e = datos["espacio"]
            print(f"\n💾 {e['usado_gb']} GB usados de {e['total_gb']} GB "
                  f"(libre: {e['libre_gb']} GB)")
            print("\n🐘 Archivos más grandes (zonas intocables respetadas):")
            for a in datos["archivos_grandes"]:
                print(f"   {a['mb']:>8} MB  {a['ruta']}")
            snap = scanner.guardar_snapshot(datos)
            print(f"\n📊 Snapshot guardado: {snap.name}")
            if input("🤖 ¿Análisis de la IA? (s/n): ").strip().lower() == "s":
                print(ia.interpretar_evidencia(
                    json.dumps(datos, ensure_ascii=False)))
        elif op == "4":
            for a in scanner.autodiagnostico():
                print("⚠️ ", a)
        elif op == "5":
            print("👋 Hasta pronto, Blumix.")
            break
        else:
            print("❌ Opción inválida: escribe un número del menú.")


if __name__ == "__main__":
    main()
