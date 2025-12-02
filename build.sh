#!/bin/bash
# Build script - package the game with PyInstaller (Linux/Mac)

echo ""
echo "========================================"
echo "  BUILD - RAYMAN ENGINE (Linux/Mac)"
echo "========================================"
echo ""

echo "[1/3] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no esta instalado"
    echo "Instala Python desde https://www.python.org"
    exit 1
fi

echo "[2/3] Instalando PyInstaller..."
python3 -m pip install --upgrade pyinstaller
if [ $? -ne 0 ]; then
    echo "ERROR: Fallo al instalar PyInstaller"
    exit 1
fi

echo "[3/3] Generando ejecutable con PyInstaller..."
python3 -m PyInstaller --noconfirm --onefile --name RaymanEngine main.py
if [ $? -ne 0 ]; then
    echo "ERROR: PyInstaller fallo al empaquetar"
    exit 1
fi

echo ""
echo "Build completado. Ejecutable generado en: dist/RaymanEngine"
