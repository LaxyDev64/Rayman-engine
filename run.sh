#!/bin/bash
# Script para instalar y ejecutar el Rayman Engine (Linux/Mac)

echo ""
echo "========================================"
echo "  RAYMAN ENGINE - Fangame 2D"
echo "========================================"
echo ""

echo "[1/3] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no esta instalado"
    echo "Instala Python desde https://www.python.org"
    exit 1
fi

echo "[2/3] Instalando dependencias..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Fallo en la instalacion de dependencias"
    exit 1
fi

echo "[3/3] Iniciando juego..."
echo ""
python3 main.py

echo ""
read -p "Presiona Enter para salir..."
