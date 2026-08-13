#!/usr/bin/env bash

SALIDA="BLUMCL-PROYECTO-COMPLETO.txt"

{
    echo "========================================"
    echo "        BLUMCL - PROYECTO COMPLETO"
    echo "========================================"
    echo
    echo "Fecha:"
    date
    echo
    echo "========================================"
    echo "ESTRUCTURA DEL PROYECTO"
    echo "========================================"
    find . \
        -not -path './.git/*' \
        -not -path './__pycache__/*' \
        -not -path '*/__pycache__/*' \
        -not -path './.pytest_cache/*' \
        -not -path '*/.pytest_cache/*' \
        -not -path './logs/*' \
        -type f | sort

    echo
    echo "========================================"
    echo "CONTENIDO DE LOS ARCHIVOS"
    echo "========================================"

    find . \
        -not -path './.git/*' \
        -not -path './__pycache__/*' \
        -not -path '*/__pycache__/*' \
        -not -path './.pytest_cache/*' \
        -not -path '*/.pytest_cache/*' \
        -not -path './logs/*' \
        -type f \
        \( \
        -name '*.py' -o \
        -name '*.md' -o \
        -name '*.json' -o \
        -name '*.toml' -o \
        -name '*.yaml' -o \
        -name '*.yml' -o \
        -name '*.txt' -o \
        -name '*.sh' \
        \) | sort | while read -r archivo
    do
        echo
        echo
        echo "########################################"
        echo "# ARCHIVO: $archivo"
        echo "########################################"
        echo
        cat "$archivo"
    done

} > "$SALIDA"

echo
echo "========================================"
echo "Archivo creado:"
echo "$SALIDA"
echo "========================================"
echo
wc -l "$SALIDA"
du -h "$SALIDA"
