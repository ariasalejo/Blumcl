#!/data/data/com.termux/files/usr/bin/bash
# ==================================================
#  BLUMCL · instalador oficial (Termux/Android)
#  Regalo de CryptoEduar (Blumix) · Copacabana, Colombia
#  Uso: bash install.sh
# ==================================================
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
PREFIX_BIN="${PREFIX:-/data/data/com.termux/files/usr}/bin"

echo "🚀 BLUMCL · instalador"
echo "   origen: $REPO"
echo

if ! command -v python >/dev/null 2>&1; then
  echo "📦 [1/4] Instalando python..."
  pkg install -y python
else
  echo "✅ [1/4] $(python -V 2>&1) presente"
fi

if [ -s "$REPO/requirements.txt" ]; then
  echo "📦 [2/4] Dependencias de requirements.txt..."
  python -m pip install --quiet -r "$REPO/requirements.txt"
else
  echo "✅ [2/4] Cero dependencias externas (100% stdlib)"
fi

echo "🔗 [3/4] Creando comando global 'blumcl'..."
mkdir -p "$PREFIX_BIN"
cat > "$PREFIX_BIN/blumcl" <<WRAP
#!/system/bin/sh
exec python "$REPO/app.py" "$@"
WRAP
chmod +x "$PREFIX_BIN/blumcl"

if command -v blumcl >/dev/null 2>&1; then
  echo "✅ [4/4] Comando verificado en el sistema"
  echo
  echo "🎉 Listo. Ejecuta: blumcl"
else
  echo "⚠️  [4/4] Reabre la terminal para activar el PATH"
fi
