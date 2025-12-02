# COMPILACION - RAYMAN ENGINE

Lamentablemente, Python embebido tiene limitaciones con pip y no permite instalar paquetes fácilmente.

## OPCION 1: Usar Instalador Python Global (RECOMENDADO)

Instala Python globalmente desde: https://www.python.org

**IMPORTANTE:** Durante la instalación:
- ☑ Marca "Add Python to PATH"  
- ☑ Instala pip

Luego ejecuta en PowerShell (como admin):
```powershell
cd "c:\Users\hecto\OneDrive\Desktop\rayman engine\RaymanEngine"
pip install pygame pyinstaller
python -m PyInstaller --onefile --name RaymanEngine main.py
```

El ejecutable se genera en: `dist\RaymanEngine.exe`

## OPCION 2: Usar el juego directamente (sin compilar)

Si quieres jugar sin compilar a .exe:

```powershell
# Instala Python global (como arriba)
pip install -r requirements.txt
python main.py
```

## OPCION 3: Generar EXE con cx_Freeze

Alternativa a PyInstaller:
```powershell
pip install cx_Freeze
cxfreeze main.py --target-dir dist
```

## Por qué Python embebido no funciona

- No incluye pip por defecto
- Limitado para instalar packages desde binarios
- Mejor solo para aplicaciones portátiles sin dependencias externas

## Resumen

**Para compilar a ejecutable unico:**
1. Instala Python global desde python.org
2. Ejecuta: `pip install pygame pyinstaller`
3. Ejecuta: `python -m PyInstaller --onefile main.py`
4. Resultado: `dist\RaymanEngine.exe` (~150MB)

Este archivo contiene Python + pygame + tu juego completo.
