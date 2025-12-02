@echo off
REM ========================================
REM   RAYMAN ENGINE - COMPILADOR
REM   Genera ejecutable RaymanEngine.exe
REM ========================================

setlocal enabledelayedexpansion

set PYTHON_EXE=C:\Program Files\Python311\python.exe
set PIP_EXE=C:\Program Files\Python311\Scripts\pip.exe

cls
echo.
echo ========================================
echo   RAYMAN ENGINE COMPILADOR v0.2.0
echo ========================================
echo.

REM Verificar si Python esta instalado
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python no encontrado en %PYTHON_EXE%
    echo.
    echo SOLUCION:
    echo ===========
    echo 1. Descarga Python desde:
    echo    https://www.python.org/downloads/
    echo.
    echo 2. Durante la instalacion MARCA estas opciones:
    echo    [X] Add Python to PATH
    echo    [X] Install pip
    echo    [X] Install for all users (recomendado)
    echo.
    echo 3. Reinicia Windows completamente
    echo.
    echo 4. Luego ejecuta este archivo nuevamente
    echo.
    pause
    exit /b 1
)

echo [1/4] Python encontrado!
"%PYTHON_EXE%" -V

echo [2/4] Instalando dependencias...
"%PIP_EXE%" install pygame pyinstaller pillow --quiet
if errorlevel 1 (
    echo ERROR: Fallo al instalar dependencias
    echo Intenta manualmente:
    echo   pip install pygame pyinstaller pillow
    pause
    exit /b 1
)

echo [3/4] Limpiando builds anteriores...
if exist dist rmdir /s /q dist >nul 2>&1
if exist build rmdir /s /q build >nul 2>&1
if exist RaymanEngine.spec del RaymanEngine.spec >nul 2>&1

echo [4/4] Compilando ejecutable...
"%PYTHON_EXE%" -m PyInstaller --noconfirm --onefile ^
    --name RaymanEngine ^
    --console ^
    --icon "assets/sprites/PC-_-Computer-Rayman-Legends-Exclusive-Content_-Wii-U-HOME-Menu-Icon.ico" ^
    --add-data "assets;assets" ^
    --add-data "src;src" ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: PyInstaller fallo
    pause
    exit /b 1
)

echo.
echo ========================================
echo   COMPILACION EXITOSA!
echo ========================================
echo.
echo Ejecutable: dist\RaymanEngine.exe
echo.
echo Para ejecutar:
echo   1. Doble click en: dist\RaymanEngine.exe
echo      o
echo   2. En terminal: .\dist\RaymanEngine.exe
echo.
pause
