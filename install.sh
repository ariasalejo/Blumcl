#!/data/data/com.termux/files/usr/bin/bash

set -e

APP_DIR="$HOME/.local/share/blumcl"
BIN_DIR="$PREFIX/bin"

echo "🚀 Instalando Blumcl..."

mkdir -p "$APP_DIR"

cp app.py "$APP_DIR/app.py"

cat > "$BIN_DIR/blumcl" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec python "$APP_DIR/app.py" "\$@"
EOF

chmod +x "$BIN_DIR/blumcl"

echo
echo "✅ Blumcl instalado correctamente."
echo "👉 Ejecuta: blumcl"
