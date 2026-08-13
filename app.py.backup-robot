#!/usr/bin/env python
"""Blumcl · Terminal de Mando v0.5.0."""

import json
import shutil
from pathlib import Path

from blumcl.ai import IALocal
from blumcl.scanners.storage import scanner
from blumcl.utils.config import cargar

VERSION = "0.5.1"

TIPS = {
    "1": "💡 Un snapshot es una foto con fecha: tu reconstrucción cronológica.",
    "2": "💡 El informe es autocontenido: con modo avión sigue vivo.",
    "3": "💡 Comparar = ver qué cambió entre dos fotos del sistema.",
    "4": "💡 Evidencia antes que acción: tu regla de oro.",
    "5": "💡 Tu IA responde sin internet: nadie lee tus preguntas.",
    "6": "💡 El autodiagnóstico sugiere; jamás borra sin tu sí.",
    "7": "💡 Dry-run: ensayar sin tocar. Así trabajan los pros.",
    "8": "💡 Las zonas intocables son tu cinturón de seguridad.",
    "9": "💡 La config se regenera sola si se daña.",
}


def cabecera():
    from blumcl.ui.banner import cabecera as banner_resp
    try:
        e = scanner.espacio()
        disco = f"💾 {e['libre_gb']} GB libres de {e['total_gb']} GB"
    except Exception:
        disco = "💾 disco: n/d"
    print(banner_resp(disco, VERSION))


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



ROBOTS = [
    [
        "        ╭──────╮        ",
        "        │ ◉  ◉ │        ",
        "        │  ╲╱  │        ",
        "     ╭──┴──────┴──╮     ",
        "     │  BLUMIX   │      ",
        " ╭───┤   CORE    ├───╮  ",
        " │   ╰────┬─────╯   │  ",
        " │        │         │  ",
        " ╰────┬───┴───┬─────╯  ",
        "      ╰───┬───╯        ",
        "          ╰             ",
    ],
    [
        "        ╭──────╮        ",
        "        │ ●  ● │        ",
        "        │  ──  │        ",
        "     ╭──┴──────┴──╮     ",
        "     │  BLUMCL    │     ",
        " ╭───┤   AI CORE  ├───╮ ",
        " │   ╰────┬───────╯   │ ",
        " │     ╭──┴──╮        │ ",
        " ╰─────┤ ╲╱  ├────────╯ ",
        "       ╰──┬──╯          ",
        "          ╰             ",
    ],
    [
        "        ╭──────╮        ",
        "        │ ◉  ◉ │        ",
        "        │  ▔▔  │        ",
        "   ╭────┴──────┴────╮   ",
        "   │   B L U M I X  │   ",
        "╭──┤    SECURITY    ├──╮",
        "│  ╰──────┬─────────╯  │",
        "│       ╭─┴─╮          │",
        "╰───────┤ ◇ ├──────────╯",
        "        ╰─┬─╯           ",
        "          ╵             ",
    ],
]

MENU_CORTO = """
  [1] 🔬 Escanear
  [2] 📊 Informe HTML
  [3] ⏳ Comparar
  [4] 🗂️  Historial
  [5] 🤖 Preguntar IA
  [6] 🩺 Autodiagnóstico
  [7] 🧹 Limpieza dry-run
  [8] 🛡️  Zonas protegidas
  [9] ⚙️  Configuración
  [0] 👋 Salir
"""


def _dw(s):
    from unicodedata import east_asian_width as ew
    return sum(2 if ew(c) in "WF" else 1 for c in s)


def menu_con_robot():
    import random
    from blumcl.ui.banner import ancho_terminal
    w = ancho_terminal()
    opciones = [MENU if w >= 64 else MENU_CORTO, MENU_CORTO]
    for menu in opciones:
        lineas = menu.strip("\n").split("\n")
        maxl = max(_dw(l) for l in lineas)
        if w >= maxl + 3 + 13:
            elegido = random.choice(ROBOTS)
            return "\n".join(
                l + " " * (maxl + 3 - _dw(l)) +
                (elegido[i] if i < len(elegido) else "")
                for i, l in enumerate(lineas))
    return "\n".join(MENU_CORTO.strip("\n").split("\n"))


def seccion(titulo):
    from blumcl.ui.banner import ancho_terminal
    w = ancho_terminal()
    print()
    print(f"\033[96m{'─' * w}\033[0m")
    print(f"\033[1m  {titulo}\033[0m")
    print(f"\033[96m{'─' * w}\033[0m")


def leer(prompt):
    """Reset de color ANSI antes de pedir entrada: nunca letra invisible."""
    return input("\033[0m" + prompt)


def ofrecer_reporte(datos):
    from blumcl.reports.html import generar
    out = generar(datos)
    print("📄 Reporte generado:", out)
    if leer("📥 ¿Descargar tu reporte? (y/n): ").strip().lower() == "y":
        copia = Path.home() / "storage" / "shared" / "Download" / "informe.html"
        shutil.copy(out, copia)
        print("✅ En Download → Archivos → Download → informe.html → Chrome.")


def main():
    ia = IALocal()
    while True:
        cabecera()
        print(menu_con_robot())
        op = leer("→ ").strip()

        if op == "1":
            print("\n🔬 Observando (sin modificar)...")
            print("📂 Leyendo tu home...")
            datos = scanner.analizar()
            print("🐘 Ordenando hallazgos...")
            e = datos["espacio"]
            print(f"\n💾 {e['usado_gb']} GB usados de {e['total_gb']} GB")
            print("\n🐘 Archivos más grandes:")
            for a in datos["archivos_grandes"]:
                print(f"   {a['mb']:>8} MB  {a['ruta']}")
            snap = scanner.guardar_snapshot(datos)
            print(f"\n📊 Snapshot: {snap.name}")
            ofrecer_reporte(datos)
            if leer("🤖 ¿Análisis de la IA? (s/n): ").strip().lower() == "s":
                print(ia.interpretar_evidencia(
                    json.dumps(datos, ensure_ascii=False)))
        elif op == "2":
            snaps = sorted(scanner.SNAPSHOTS.glob("*.json"))
            if not snaps:
                print("❌ No hay snapshots: usa la opción 1.")
            else:
                ofrecer_reporte(json.loads(snaps[-1].read_text()))
        elif op == "3":
            from blumcl.analysis import comparar as comp
            print("\n⏳ " + (comp.comparar()
                  or "ℹ️ Necesito 2 snapshots: vuelve a escanear (opción 1)."))
        elif op == "4":
            from blumcl.analysis import comparar as comp
            snaps = comp.listar()
            print(f"\n🗂️  Historial: {len(snaps)} snapshots")
            for s in snaps:
                print("   📊", s.name)
        elif op == "5":
            q = leer("Tu pregunta: ").strip()
            if q:
                print("\n🤖 Pensando...\n")
                print(ia.preguntar(q, 300))
        elif op == "6":
            seccion("🩺 AUTODIAGNÓSTICO")
            avisos = scanner.autodiagnostico()
            if not avisos:
                print("\n  🟢 Sin avisos: todo en orden.")
            for a in avisos:
                print(f"\n  ⚠️  {a}")
            print(f"\n  📋 {len(avisos)} aviso(s) · 0 acciones automáticas")
        elif op == "7":
            from blumcl.cleaner import controlled as cl
            cand = cl.plan()
            if not cand:
                print("🟢 Nada que sugerir.")
            else:
                print("\n🧹 Candidatos a limpieza controlada:")
                for n, c in enumerate(cand, 1):
                    print(f"   {n}) {c}")
                sel = leer("→ Cuál gestionas (número, 0=salir): ").strip()
                if sel.isdigit() and 1 <= int(sel) <= len(cand):
                    ruta = cand[int(sel) - 1]
                    print(f"\n⚠️  {ruta}")
                    print("   Se MOVERÁ a ~/blumcl_papelera (recuperable).")
                    if leer("   Escribe SI para confirmar: ").strip() == "SI":
                        print("✅ En cuarentena:", cl.cuarentena(ruta))
                    else:
                        print("🛡️  Cancelado. Nada se tocó.")
        elif op == "8":
            cfg = cargar()
            print("\n🛡️  Zonas intocables:")
            for z in cfg["zonas_intocables"]:
                print("   🔒", z)
        elif op == "9":
            from blumcl.utils import config as cfgmod
            cfg = cargar()
            print("\n⚙️  Gestión de configuración:")
            print("   1) Ver todo")
            print("   2) Añadir zona intocable")
            print("   3) Quitar zona intocable")
            sub = leer("→ ").strip()
            if sub == "1":
                print(json.dumps(cfg, ensure_ascii=False, indent=2))
            elif sub == "2":
                z = input("Nueva zona: ").strip()
                if z and z not in cfg["zonas_intocables"]:
                    cfg["zonas_intocables"].append(z)
                    cfgmod.guardar(cfg)
                    print(f"🔒 {z} ahora es intocable.")
            elif sub == "3":
                z = input("Zona a quitar: ").strip()
                if z in cfg["zonas_intocables"]:
                    cfg["zonas_intocables"].remove(z)
                    cfgmod.guardar(cfg)
                    print(f"🔓 {z} ya no es intocable.")
        elif op == "0":
            print("👋 Hasta pronto, Blumix.")
            break
        else:
            print("❌ Opción inválida.")

        if op in TIPS:
            leer(f"\n{TIPS[op]}\n⏸️  Enter para continuar...")
            from blumcl.ui.banner import frase_seguridad, ancho_terminal
            print()
            frase_seguridad(ancho_terminal())
            print()


if __name__ == "__main__":
    main()
