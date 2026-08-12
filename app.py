#!/usr/bin/env python3

APP_NAME = "Termux Cleaner"
VERSION = "0.1.0"


def mostrar_menu():
    print()
    print("╔══════════════════════════════════╗")
    print(f"║        🚀 {APP_NAME:<19}║")
    print(f"║        Versión {VERSION:<13}║")
    print("╠══════════════════════════════════╣")
    print("║  1. 🔎 Analizar                  ║")
    print("║  2. 📊 Ver espacio               ║")
    print("║  3. 🧹 Limpiar                   ║")
    print("║  4. 📋 Generar informe           ║")
    print("║  5. ❌ Salir                     ║")
    print("╚══════════════════════════════════╝")


def main():
    mostrar_menu()


if __name__ == "__main__":
    main()
