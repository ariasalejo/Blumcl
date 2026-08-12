"""Blumcl · informe HTML autocontenido (sin internet)."""

import json
from pathlib import Path

RAIZ = Path(__file__).parents[2]


def _barra(valor, total, color):
    pct = round(valor / total * 100, 1) if total else 0
    return (f'<div style="background:#3E4451;border-radius:6px;'
            f'height:22px;overflow:hidden;">'
            f'<div style="background:{color};width:{pct}%;height:100%;'
            f'color:#fff;font:600 12px system-ui;padding-left:8px;'
            f'line-height:22px;">{pct}%</div></div>')


def generar(datos, nombre=None):
    e = datos["espacio"]
    lleno = e["usado_gb"] / e["total_gb"] > 0.9
    filas = "".join(
        f"<tr><td style='padding:8px;border-bottom:1px solid #3E4451;'>"
        f"{a['mb']:.1f} MB</td><td style='padding:8px;"
        f"border-bottom:1px solid #3E4451;word-break:break-all;"
        f"font-size:12px;'>{a['ruta']}</td></tr>"
        for a in datos["archivos_grandes"])

    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<title>Blumcl · {datos['fecha']}</title></head>
<body style="background:#282C34;color:#DCDFE4;font-family:system-ui;
max-width:900px;margin:40px auto;padding:20px;">
<h1 style="color:#56B6C2;border-bottom:2px solid #56B6C2;">
🚀 Blumcl · Informe</h1>
<p>📅 {datos['fecha']}</p>
<div style="background:#21252B;border-radius:10px;padding:20px;">
<h2 style="color:#C678DD;">💾 Almacenamiento</h2>
<p>Total <b>{e['total_gb']} GB</b> · Usado <b>{e['usado_gb']} GB</b> ·
Libre <b>{e['libre_gb']} GB</b></p>
{_barra(e['usado_gb'], e['total_gb'], '#E06C75' if lleno else '#98C379')}
</div>
<div style="background:#21252B;border-radius:10px;padding:20px;margin-top:15px;">
<h2 style="color:#C678DD;">🐘 Archivos más grandes</h2>
<table style="width:100%;border-collapse:collapse;">
<tr><th style="text-align:left;padding:10px;background:#3E4451;
color:#E5C07B;">Tamaño</th><th style="text-align:left;padding:10px;
background:#3E4451;color:#E5C07B;">Ruta</th></tr>{filas}</table>
<p style="color:#5C6370;font-size:12px;">🔒 Zonas intocables respetadas.</p>
</div>
<p style="text-align:center;color:#5C6370;font-size:12px;margin-top:40px;">
Generado por Blumcl v0.3.0 · IA local · Sin internet</p>
</body></html>"""

    out = RAIZ / "reports" / "html" / (nombre or "informe.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out
