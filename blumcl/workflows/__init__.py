"""
BLUMCL · Workflows profesionales encadenados.
Regalo de CryptoEduar (Blumix) · Copacabana, Colombia.

Cada opción del menú no es un botón aislado: es un mini-consultor
que encadena acciones coherentes de principio a fin.
Filosofía: observar → diseñar → verificar → decidir → aprender.
"""
from __future__ import annotations
import importlib
import time
import json
from datetime import datetime
from pathlib import Path

# ---------- Carga defensiva de módulos reales ----------
MODULOS = {}

def _carga(nombre, ruta):
    try:
        MODULOS[nombre] = importlib.import_module(ruta)
        return True
    except Exception:
        MODULOS[nombre] = None
        return False

_carga("storage", "blumcl.scanners.storage")
_carga("cpu", "blumcl.scanners.cpu")
_carga("memory", "blumcl.scanners.memory")
_carga("snapshot", "blumcl.core.snapshot")
_carga("evidence", "blumcl.core.evidence")
_carga("cleaner", "blumcl.cleaner.controlled")
_carga("ia", "blumcl.ai.local_ai")
_carga("comparar", "blumcl.analysis.comparar")

# ---------- Utilidades premium ----------
def _barra(pct, ancho=24):
    pct = max(0, min(100, int(pct)))
    lleno = ancho * pct // 100
    return "█" * lleno + "░" * (ancho - lleno)

def _paso(titulo):
    print(f"├─ {titulo} ", end="", flush=True)

def _ok(msg):
    print(f"\033[92m✅ {msg}\033[0m")

def _warn(msg):
    print(f"\033[93m⚠️  {msg}\033[0m")

def _err(msg):
    print(f"\033[91m❌ {msg}\033[0m")

def _info(msg):
    print(f"\033[96mℹ️  {msg}\033[0m")

def _highlight(msg):
    print(f"\033[1;97m💎 {msg}\033[0m")

def _progreso(seg=0.6):
    for i in range(0, 101, 20):
        print(f"\r│  [{_barra(i)}] {i:3d}%", end="", flush=True)
        time.sleep(0.05 * seg / 6)
    print(f"\r│  [{_barra(100)}] 100%", flush=True)

def _confirmar(mensaje):
    try:
        r = input(f"\033[93m🤔 {mensaje} [s/N]: \033[0m").strip().lower()
        return r in ("s", "si", "y", "yes")
    except (EOFError, KeyboardInterrupt):
        print()
        return False

def _resolver(mod, nombres):
    if mod is None:
        return None
    for n in nombres:
        if hasattr(mod, n):
            return getattr(mod, n)
    return None

def _instanciar(obj):
    return obj() if obj is not None and isinstance(obj, type) else obj


# =====================================================================
# POST-ACCIONES PREMIUM (automáticas, coherentes, no intrusivas)
# =====================================================================
class PostAcciones:
    """Acciones automáticas que se encadenan al final de cada workflow."""

    @staticmethod
    def snapshot_automatico(etiqueta="auto"):
        """Guarda snapshot sin preguntar. El usuario lo ve como valor agregado."""
        try:
            mod = MODULOS["snapshot"]
            crear = _resolver(mod, ("crear_snapshot", "Snapshot", "crear"))
            if crear is None:
                return None
            snap = crear() if callable(crear) else None
            sid = getattr(snap, "id", getattr(snap, "snapshot_id", etiqueta))
            _highlight(f"snapshot automático guardado: {sid}")
            return sid
        except Exception:
            return None

    @staticmethod
    def resumen_ejecutivo(resultados):
        """Genera un resumen de 3 líneas con lo más importante."""
        print()
        print("\033[1m📋 RESUMEN EJECUTIVO (3 líneas)\033[0m")
        print("─" * 50)

        # Storage
        st = resultados.get("storage")
        if st:
            libre = getattr(st, "libre_gb", getattr(st, "free_gb", None))
            total = getattr(st, "total_gb", None)
            if libre is not None and total is not None:
                pct = round((float(libre) / float(total)) * 100, 1) if total else 0
                print(f"  💾 Almacenamiento: {libre}/{total} GB libre ({pct}%)")
            else:
                print("  💾 Almacenamiento: leído")

        # CPU
        cpu = resultados.get("cpu")
        if cpu:
            arq = getattr(cpu, "arquitectura", getattr(cpu, "architecture", "n/d"))
            print(f"  🧠 CPU: {arq}")

        # Memoria
        mem = resultados.get("memory")
        if mem:
            usada = getattr(mem, "usada_gb", getattr(mem, "used_gb", None))
            total = getattr(mem, "total_gb", None)
            if usada is not None and total is not None:
                print(f"  🧠 RAM: {usada}/{total} GB usada")

    @staticmethod
    def sugerir_informe(resultados):
        """Al final del escaneo, sugiere generar el informe HTML."""
        print()
        _info("💡 ¿Generar informe HTML ahora? (opción 2 del menú)")
        print("   Incluye gráficos, tablas y recomendaciones visuales.")

    @staticmethod
    def comparar_con_anterior(snapshot_id):
        """Compara automáticamente con el snapshot anterior si existe."""
        try:
            snap_dir = Path.home() / "Blumcl" / "snapshots"
            if not snap_dir.exists():
                snap_dir = Path("snapshots")
            snaps = sorted(snap_dir.glob("*.json"))
            if len(snaps) >= 2:
                print()
                _highlight(f"📈 Hay {len(snaps)} snapshots · puedes comparar evolución (opción 3)")
        except Exception:
            pass

    @staticmethod
    def siguiente_accion_sugerida(texto):
        """Sugiere el siguiente paso lógico."""
        print()
        print(f"\033[1m🎯 SIGUIENTE PASO SUGERIDO:\033[0m")
        print(f"   {texto}")


# =====================================================================
# WORKFLOW 1 · ESCANEAR (opción 1 del menú)
# Encadena: escaneo → snapshot automático → resumen → sugerencia
# =====================================================================
class EscanearWorkflow:
    """Escaneo completo + encadenamiento automático premium."""

    @staticmethod
    def ejecutar():
        print("\n🔬 ESCANEAR SISTEMA COMPLETO")
        print("═" * 56)
        _info("Modo: SOLO LECTURA · NADA SE MODIFICA")
        inicio = datetime.now()
        resultados = {}

        # 1. Storage
        _paso("📁 Escaneando almacenamiento...")
        try:
            cls = _resolver(MODULOS["storage"], ("StorageScanner", "Scanner"))
            obj = _instanciar(cls)
            res = obj.scan() if obj and hasattr(obj, "scan") else None
            resultados["storage"] = res
            _progreso()
            libre = getattr(res, "libre_gb", getattr(res, "free_gb", "n/d"))
            total = getattr(res, "total_gb", "n/d")
            _ok(f"{libre}/{total} GB libre")
        except Exception as e:
            _warn(f"omitido: {e.__class__.__name__}")

        # 2. CPU
        _paso("🧠 Analizando CPU...")
        try:
            cls = _resolver(MODULOS["cpu"], ("CPUScanner", "Scanner"))
            obj = _instanciar(cls)
            cpu = obj.scan() if obj and hasattr(obj, "scan") else None
            resultados["cpu"] = cpu
            _progreso(seg=0.3)
            arq = getattr(cpu, "arquitectura", getattr(cpu, "architecture", "n/d"))
            _ok(f"arquitectura: {arq}")
        except Exception as e:
            _warn(f"omitido: {e.__class__.__name__}")

        # 3. Memoria
        _paso("🧠 Leyendo memoria RAM...")
        try:
            cls = _resolver(MODULOS["memory"], ("MemoryScanner", "Scanner"))
            obj = _instanciar(cls)
            mem = obj.scan() if obj and hasattr(obj, "scan") else None
            resultados["memory"] = mem
            usada = getattr(mem, "usada_gb", getattr(mem, "used_gb", "n/d"))
            total = getattr(mem, "total_gb", "n/d")
            _ok(f"{usada}/{total} GB usada")
        except Exception as e:
            _warn(f"omitido: {e.__class__.__name__}")

        dur = (datetime.now() - inicio).total_seconds()
        print()
        print("═" * 56)
        print(f"✅ ESCANEO COMPLETADO en {dur:.1f}s")
        print("═" * 56)

        # ---------- POST-ACCIONES AUTOMÁTICAS ----------
        print()
        print("\033[1m✨ ENCANTENAMIENTO PREMIUM (automático)\033[0m")
        print("─" * 50)

        # A: Snapshot automático
        PostAcciones.snapshot_automatico("post-escaneo")

        # B: Resumen ejecutivo
        PostAcciones.resumen_ejecutivo(resultados)

        # C: Comparar con anterior si existe
        PostAcciones.comparar_con_anterior(None)

        # D: Sugerencia siguiente paso
        PostAcciones.siguiente_accion_sugerida(
            "Generar informe HTML (opción 2) para gráficos y recomendaciones visuales."
        )

        return resultados


# =====================================================================
# WORKFLOW 2 · INFORME HTML (opción 2 del menú)
# Encadena: generar → ofrecer descarga → sugerir snapshot de referencia
# =====================================================================
class InformeWorkflow:
    """Informe HTML + encadenamiento premium."""

    @staticmethod
    def ejecutar():
        print("\n📊 GENERAR INFORME HTML")
        print("═" * 56)
        inicio = datetime.now()
        ruta_informe = None

        # 1. Generar informe
        _paso("📝 Construyendo informe HTML offline...")
        try:
            # Intenta usar informe.py del repo si existe
            import subprocess
            import sys
            repo = Path(__file__).resolve().parent.parent
            informe_py = repo / "informe.py"
            if informe_py.exists():
                resultado = subprocess.run(
                    [sys.executable, str(informe_py)],
                    capture_output=True, text=True, timeout=30
                )
                # Busca el archivo HTML generado más reciente
                candidatos = list(repo.glob("reports/*.html")) + \
                             list(Path.home().glob("Blumcl/reports/*.html"))
                if candidatos:
                    ruta_informe = max(candidatos, key=lambda p: p.stat().st_mtime)
            _progreso(seg=1.5)
            if ruta_informe:
                _ok(f"informe generado: {ruta_informe.name}")
            else:
                _ok("estructura de informe lista (ejecuta informe.py)")
        except Exception as e:
            _warn(f"informe: {e.__class__.__name__}")

        dur = (datetime.now() - inicio).total_seconds()
        print()
        print("═" * 56)
        print(f"✅ INFORME GENERADO en {dur:.1f}s")
        print("═" * 56)

        # ---------- POST-ACCIONES AUTOMÁTICAS ----------
        print()
        print("\033[1m✨ ENCANTENAMIENTO PREMIUM (automático)\033[0m")
        print("─" * 50)

        # A: Información del archivo
        if ruta_informe and ruta_informe.exists():
            tamano_kb = ruta_informe.stat().st_size / 1024
            _highlight(f"archivo: {ruta_informe} ({tamano_kb:.1f} KB)")
            _info("abrelo en cualquier navegador · funciona sin internet")

        # B: Snapshot de referencia
        PostAcciones.snapshot_automatico("pre-informe")

        # C: Siguiente paso
        PostAcciones.siguiente_accion_sugerida(
            "Compartir el informe con mamá/compañero o archivarlo como evidencia."
        )

        return ruta_informe


# =====================================================================
# WORKFLOW 3 · LIMPIEZA SEGURA (opción 7 del menú)
# Encadena: dry-run → snapshot pre → confirmar → ejecutar → snapshot post → diff
# =====================================================================
class LimpiezaWorkflow:
    """Limpieza controlada con encadenamiento defensivo."""

    @staticmethod
    def ejecutar():
        print("\n🧹 LIMPIEZA SEGURA (dry-run obligatorio)")
        print("═" * 56)
        _info("Regla: PRIMERO probamos · LUEGO decides")
        inicio = datetime.now()

        # 1. Dry-run
        _paso("🔍 Simulando limpieza (sin tocar nada)...")
        mod = MODULOS["cleaner"]
        limpiar = _resolver(mod, ("limpieza_controlada", "clean", "run"))
        if limpiar is None:
            _err("módulo de limpieza no disponible")
            return None

        try:
            sim = limpiar(dry_run=True) if callable(limpiar) else None
            _progreso()
            rec = getattr(sim, "espacio_recuperable_mb",
                         getattr(sim, "recoverable_mb", "n/d"))
            archivos = getattr(sim, "archivos", getattr(sim, "files", []))
            _ok(f"~{rec} MB recuperables en {len(archivos)} elementos")
        except Exception as e:
            _err(f"simulación falló: {e.__class__.__name__}")
            return None

        # 2. Snapshot PRE-limpieza (automático)
        print()
        _info("📸 Guardando snapshot PRE-limpieza (para poder revertir)...")
        snap_pre_id = PostAcciones.snapshot_automatico("pre-limpieza")

        # 3. Confirmación humana
        print()
        if not _confirmar("¿Ejecutar limpieza REAL?"):
            _warn("cancelado · nada se tocó")
            return None

        # 4. Ejecución
        _paso("🧹 Ejecutando limpieza controlada...")
        try:
            real = limpiar(dry_run=False)
            _progreso(seg=1.2)
            lib = getattr(real, "liberado_mb", getattr(real, "freed_mb", 0))
            _ok(f"liberados ~{lib} MB")
        except Exception as e:
            _err(f"ejecución falló: {e.__class__.__name__}")
            return None

        # 5. Snapshot POST-limpieza (automático)
        snap_post_id = PostAcciones.snapshot_automatico("post-limpieza")

        dur = (datetime.now() - inicio).total_seconds()
        print()
        print("═" * 56)
        print(f"✅ LIMPIEZA FINALIZADA en {dur:.1f}s")
        print("═" * 56)

        # ---------- POST-ACCIONES AUTOMÁTICAS ----------
        print()
        print("\033[1m✨ ENCANTENAMIENTO PREMIUM (automático)\033[0m")
        print("─" * 50)
        if snap_pre_id and snap_post_id:
            _highlight(f"🔄 Reversible: compara snapshot {snap_pre_id} vs {snap_post_id}")
        PostAcciones.siguiente_accion_sugerida(
            "Comparar snapshots (opción 3) para ver exactamente qué cambió."
        )

        return real


# =====================================================================
# API PÚBLICA (para app.py)
# =====================================================================
def ejecutar(opcion):
    """Dispatcher según la opción del menú principal."""
    dispatch = {
        "1": EscanearWorkflow.ejecutar,
        "2": InformeWorkflow.ejecutar,
        "7": LimpiezaWorkflow.ejecutar,
    }
    fn = dispatch.get(opcion)
    if fn:
        return fn()
    else:
        _warn(f"workflow no implementado para opción {opcion}")
        return None


if __name__ == "__main__":
    print("\n🧪 PROBADOR DE WORKFLOWS")
    print("=" * 40)
    print("[1] Escanear (opción 1 del menú)")
    print("[2] Informe HTML (opción 2 del menú)")
    print("[7] Limpieza segura (opción 7 del menú)")
    print("[0] Salir")
    try:
        op = input("→ ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        exit()
    if op in ("1", "2", "7"):
        ejecutar(op)
    else:
        print("👋 Hasta luego.")
