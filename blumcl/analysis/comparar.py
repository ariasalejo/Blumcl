"""Blumcl · comparación de snapshots (reconstrucción cronológica)."""

import json

from blumcl.scanners.storage import scanner


def listar():
    return sorted(scanner.SNAPSHOTS.glob("*.json"))


def comparar():
    snaps = listar()
    if len(snaps) < 2:
        return None
    a = json.loads(snaps[-2].read_text())
    b = json.loads(snaps[-1].read_text())

    antes = {x["ruta"]: x["mb"] for x in a.get("archivos_grandes", [])}
    ahora = {x["ruta"]: x["mb"] for x in b.get("archivos_grandes", [])}

    lineas = []
    delta = round(b["espacio"]["usado_gb"] - a["espacio"]["usado_gb"], 2)
    lineas.append(f"💾 Usado: {a['espacio']['usado_gb']} → "
                  f"{b['espacio']['usado_gb']} GB ({delta:+} GB)")

    for r in ahora:
        if r not in antes:
            lineas.append(f"🆕 Nuevo: {ahora[r]} MB  {r}")
    for r in antes:
        if r not in ahora:
            lineas.append(f"👋 Fuera: {antes[r]} MB  {r}")
    for r in ahora:
        if r in antes and ahora[r] > antes[r]:
            lineas.append(f"📈 Creció: {antes[r]} → {ahora[r]} MB  {r}")

    if len(lineas) == 1:
        lineas.append("🟢 Sin cambios en archivos grandes.")
    return "\n".join(lineas)
