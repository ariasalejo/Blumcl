#!/usr/bin/env python
"""BLUMCL · Terminal de Mando v0.5.1."""

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
        "        ╔════════════╗        ",
        "        ║  ◈      ◈ ║        ",
        "        ║     ▄      ║        ",
        "     ╔══╩════════════╩══╗     ",
        "     ║   ╔══════════╗   ║     ",
        " ╔═══╩═══╣  BLUMIX  ╠═══╩═══╗ ",
        " ║       ╚════╤═════╝       ║ ",
        " ║          ╔═╧═╗           ║ ",
        " ╚══════╦═══╣ ◇ ╠═══╦══════╝ ",
        "        ║   ╚═╤═╝   ║        ",
        "        ╚═════╧═════╝        ",
        "           ╱ ╲  ╱ ╲          ",
    ],
    [
        "        ╔════════════╗        ",
        "        ║  ●      ●  ║        ",
        "        ║      ─     ║        ",
        "     ╔══╩════════════╩══╗     ",
        "     ║  ╔════════════╗  ║     ",
        " ╔═══╩══╣   B L U M  ╠══╩═══╗ ",
        " ║      ╚══════╤═════╝      ║ ",
        " ║          ╭─┴─╮          ║ ",
        " ╚══════╦═══╡ ◇ ╞═══╦══════╝ ",
        "        ║   ╰─┬─╯   ║        ",
        "        ╚═════╧═════╝        ",
        "          ╱╲    ╱╲           ",
    ],
    [
        "        ╔════════════╗        ",
        "        ║  ◉      ◉  ║        ",
        "        ║     ╲╱     ║        ",
        "     ╔══╩════════════╩══╗     ",
        "     ║   BLUMCL CORE    ║     ",
        " ╔═══╩════════╤═════════╩═══╗ ",
        " ║          ╭─┴─╮          ║ ",
        " ║       ╔══╡ ◇ ╞══╗       ║ ",
        " ╚═══════╣  ╰─┬─╯  ╠═══════╝ ",
        "         ╚════╧════╝         ",
        "          ╱ ╲  ╱ ╲           ",
        "         ╱___╲╱___╲          ",
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


def _dw(texto):
    """Calcula aproximadamente el ancho visual del texto."""
    from unicodedata import east_asian_width

    return sum(
        2 if east_asian_width(c) in "WF" else 1
        for c in texto
    )


def cabecera():
    """Muestra la cabecera principal de BLUMCL."""
    from blumcl.ui.banner import cabecera as banner_resp

    try:
        espacio = scanner.espacio()
        disco = (
            f"💾 {espacio['libre_gb']} GB libres "
            f"de {espacio['total_gb']} GB"
        )
    except Exception:
        disco = "💾 disco: n/d"

    print(banner_resp(disco, VERSION))


def _dw(s):
    from unicodedata import east_asian_width as ew
    return sum(2 if ew(c) in "WF" else 1 for c in s)


def menu_con_robot():
    """Menú principal responsivo con robot BLUMIX."""

    import random
    from blumcl.ui.banner import ancho_terminal

    w = ancho_terminal()

    menu = MENU if w >= 64 else MENU_CORTO

    lineas = menu.strip("\n").split("\n")

    maxl = max(_dw(l) for l in lineas)

    robot = random.choice(ROBOTS)

    # En terminales demasiado estrechas,
    # mostrar únicamente el menú para evitar deformaciones.
    # Umbral compacto: permite que el robot aparezca
    # sin obligar a ampliar demasiado la terminal.
    if w < maxl + 15:
        return "\n".join(lineas)

    resultado = []

    for i, linea in enumerate(lineas):
        # Separación mínima entre menú y robot.
        # Esto mantiene el menú compacto en pantallas pequeñas.
        espacio = max(1, maxl - _dw(linea) + 1)

        if i < len(robot):
            resultado.append(
                linea
                + (" " * espacio)
                + robot[i]
            )
        else:
            resultado.append(linea)

    return "\n".join(resultado)


def seccion(titulo):
    """Muestra una sección visual adaptable al terminal."""
    from blumcl.ui.banner import ancho_terminal

    ancho = ancho_terminal()

    print()
    print(f"\033[96m{'─' * ancho}\033[0m")
    print(f"\033[1m  {titulo}\033[0m")
    print(f"\033[96m{'─' * ancho}\033[0m")


def leer(prompt):
    """Solicita entrada restaurando primero el color ANSI."""
    return input("\033[0m" + prompt)


def ofrecer_reporte(datos):
    """Genera el informe y permite copiarlo a Download."""
    from blumcl.reports.html import generar

    salida = generar(datos)

    print("📄 Reporte generado:", salida)

    if leer("📥 ¿Descargar tu reporte? (y/n): ").strip().lower() == "y":
        destino = (
            Path.home()
            / "storage"
            / "shared"
            / "Download"
            / "informe.html"
        )

        shutil.copy(salida, destino)

        print(
            "✅ En Download → Archivos → Download → "
            "informe.html → Chrome."
        )


def opcion_escanear(ia):
    """Ejecuta el scanner y genera evidencia."""
    print("\n🔬 Observando (sin modificar)...")
    print("📂 Leyendo tu home...")

    datos = scanner.analizar()

    print("🐘 Ordenando hallazgos...")

    espacio = datos["espacio"]

    print(
        f"\n💾 {espacio['usado_gb']} GB usados "
        f"de {espacio['total_gb']} GB"
    )

    print("\n🐘 Archivos más grandes:")

    for archivo in datos["archivos_grandes"]:
        print(
            f"   {archivo['mb']:>8} MB  "
            f"{archivo['ruta']}"
        )

    snapshot = scanner.guardar_snapshot(datos)

    print(f"\n📊 Snapshot: {snapshot.name}")

    ofrecer_reporte(datos)

    if leer(
        "🤖 ¿Análisis de la IA? (s/n): "
    ).strip().lower() == "s":

        print(
            ia.interpretar_evidencia(
                json.dumps(
                    datos,
                    ensure_ascii=False
                )
            )
        )


def opcion_informe():
    """Genera informe usando el snapshot más reciente."""
    snapshots = sorted(
        scanner.SNAPSHOTS.glob("*.json")
    )

    if not snapshots:
        print(
            "❌ No hay snapshots: "
            "usa la opción 1."
        )
        return

    ofrecer_reporte(
        json.loads(
            snapshots[-1].read_text()
        )
    )


def opcion_comparar():
    """Compara snapshots existentes."""
    from blumcl.analysis import comparar as comp

    resultado = comp.comparar()

    print(
        "\n⏳ "
        + (
            resultado
            or "ℹ️ Necesito 2 snapshots: "
               "vuelve a escanear (opción 1)."
        )
    )


def opcion_historial():
    """Muestra el historial de snapshots."""
    from blumcl.analysis import comparar as comp

    snapshots = comp.listar()

    print(
        f"\n🗂️  Historial: "
        f"{len(snapshots)} snapshots"
    )

    for snapshot in snapshots:
        print("   📊", snapshot.name)


def opcion_ia(ia):
    """Abre una consulta a la IA local."""
    pregunta = leer(
        "Tu pregunta: "
    ).strip()

    if pregunta:
        print("\n🤖 Pensando...\n")
        print(
            ia.preguntar(
                pregunta,
                300
            )
        )


def opcion_autodiagnostico():
    """Ejecuta el autodiagnóstico."""
    seccion("🩺 AUTODIAGNÓSTICO")

    avisos = scanner.autodiagnostico()

    if not avisos:
        print(
            "\n  🟢 Sin avisos: todo en orden."
        )

    for aviso in avisos:
        print(
            f"\n  ⚠️  {aviso}"
        )

    print(
        f"\n  📋 {len(avisos)} aviso(s) "
        "· 0 acciones automáticas"
    )


def opcion_limpieza():
    """Muestra candidatos y permite cuarentena manual."""
    from blumcl.cleaner import controlled as cleaner

    candidatos = cleaner.plan()

    if not candidatos:
        print("🟢 Nada que sugerir.")
        return

    print(
        "\n🧹 Candidatos a limpieza controlada:"
    )

    for numero, candidato in enumerate(
        candidatos,
        1
    ):
        print(
            f"   {numero}) {candidato}"
        )

    seleccion = leer(
        "→ Cuál gestionas "
        "(número, 0=salir): "
    ).strip()

    if (
        seleccion.isdigit()
        and 1 <= int(seleccion) <= len(candidatos)
    ):
        ruta = candidatos[
            int(seleccion) - 1
        ]

        print(f"\n⚠️  {ruta}")

        print(
            "   Se MOVERÁ a "
            "~/blumcl_papelera "
            "(recuperable)."
        )

        confirmacion = leer(
            "   Escribe SI para confirmar: "
        ).strip()

        if confirmacion == "SI":
            print(
                "✅ En cuarentena:",
                cleaner.cuarentena(ruta)
            )
        else:
            print(
                "🛡️  Cancelado. Nada se tocó."
            )


def opcion_zonas():
    """Muestra las zonas protegidas."""
    config = cargar()

    print("\n🛡️  Zonas intocables:")

    for zona in config["zonas_intocables"]:
        print("   🔒", zona)


def opcion_configuracion():
    """Gestiona la configuración de BLUMCL."""
    from blumcl.utils import config as config_mod

    config = cargar()

    print("\n⚙️  Gestión de configuración:")
    print("   1) Ver todo")
    print("   2) Añadir zona intocable")
    print("   3) Quitar zona intocable")

    sub = leer("→ ").strip()

    if sub == "1":
        print(
            json.dumps(
                config,
                ensure_ascii=False,
                indent=2
            )
        )

    elif sub == "2":
        zona = input(
            "Nueva zona: "
        ).strip()

        if (
            zona
            and zona not in config["zonas_intocables"]
        ):
            config["zonas_intocables"].append(zona)
            config_mod.guardar(config)

            print(
                f"🔒 {zona} ahora es intocable."
            )

    elif sub == "3":
        zona = input(
            "Zona a quitar: "
        ).strip()

        if zona in config["zonas_intocables"]:
            config["zonas_intocables"].remove(zona)
            config_mod.guardar(config)

            print(
                f"🔓 {zona} ya no es intocable."
            )


def pausa(opcion):
    """Muestra el consejo de seguridad correspondiente."""
    if opcion not in TIPS:
        return

    from blumcl.ui.banner import (
        ancho_terminal,
        frase_seguridad,
    )

    leer(
        f"\n{TIPS[opcion]}\n"
        "⏸️  Enter para continuar..."
    )

    print()

    frase_seguridad(
        ancho_terminal()
    )

    print()


def main():
    """Punto principal del terminal BLUMCL."""
    ia = IALocal()

    while True:
        cabecera()

        print(menu_con_robot())

        opcion = leer(
            "→ "
        ).strip()

        if opcion == "1":
            opcion_escanear(ia)

        elif opcion == "2":
            opcion_informe()

        elif opcion == "3":
            opcion_comparar()

        elif opcion == "4":
            opcion_historial()

        elif opcion == "5":
            opcion_ia(ia)

        elif opcion == "6":
            opcion_autodiagnostico()

        elif opcion == "7":
            opcion_limpieza()

        elif opcion == "8":
            opcion_zonas()

        elif opcion == "9":
            opcion_configuracion()

        elif opcion == "0":
            print(
                "👋 Hasta pronto, Blumix."
            )
            break

        else:
            print(
                "❌ Opción inválida."
            )

        pausa(opcion)


# ============================================================
# ▶️ ENTRADA DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()
