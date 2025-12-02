# 🚀 Guía de Instalación Rápida - Rayman Engine

## Requisitos Previos

1. **Python 3.8 o superior**
2. **pip** (gestor de paquetes de Python)

## Instalación de Python (si no lo tienes)

### Windows

1. Ve a https://www.python.org/downloads/
2. Descarga la versión más reciente para Windows
3. **IMPORTANTE**: Durante la instalación, marca la opción "Add Python to PATH"
4. Completa la instalación

### macOS

```bash
# Usando Homebrew (si lo tienes instalado)
brew install python3
```

O descarga desde https://www.python.org/downloads/

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

## Instalación del Engine

### Opción 1: Script Automático (Recomendado)

**Windows:**
```bash
# Doble click en run.bat
o
cd RaymanEngine
run.bat
```

**Linux/Mac:**
```bash
cd RaymanEngine
chmod +x run.sh
./run.sh
```

### Opción 2: Manual

1. Abre una terminal/consola
2. Navega a la carpeta del proyecto:
   ```bash
   cd RaymanEngine
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta el juego:
   ```bash
   python main.py
   ```

## Verificar Instalación

Para verificar que todo está correctamente instalado, ejecuta:

```bash
python test_engine.py
```

Deberías ver algo como:
```
==================================================
PRUEBAS DEL RAYMAN ENGINE
==================================================

Probando importaciones...
✓ Config importado
✓ Engine importado
✓ Entidades importadas
✓ Escenas importadas
✓ Utilidades importadas

✓ Todas las importaciones exitosas!
...
```

## Solución de Problemas

### Error: "Python no se reconoce"

**Solución**: Asegúrate de haber marcado "Add Python to PATH" durante la instalación. Reinicia tu terminal después.

### Error: "No such file or directory: main.py"

**Solución**: Asegúrate de estar en la carpeta correcta. Ejecuta:
```bash
cd RaymanEngine
pwd  # En Linux/Mac, dir en Windows (para ver tu ubicación actual)
```

### Error: "No module named 'pygame'"

**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "pip: command not found"

**Solución**: Intenta con `pip3`:
```bash
pip3 install -r requirements.txt
python3 main.py
```

## Primeros Pasos

Una vez instalado, prueba lo siguiente:

### 1. Ejecutar las pruebas
```bash
python test_engine.py
```

### 2. Jugar el nivel inicial
```bash
python main.py
```

### 3. Explorar los ejemplos
Abre `EJEMPLOS.py` para ver cómo crear nuevas entidades y escenas.

## Comandos Útiles

```bash
# Ver versión de Python
python --version

# Instalar un paquete específico
pip install nombre_paquete

# Listar paquetes instalados
pip list

# Ver ayuda de pip
pip help
```

## Recomendaciones

1. **Usa un editor de código**: Descarga VS Code (https://code.visualstudio.com/) para mejor experiencia
2. **Virtualenv** (opcional): Si trabaja en múltiples proyectos Python, considera usar entornos virtuales:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Mantén todo actualizado**:
   ```bash
   pip install --upgrade pygame
   ```

## ¿Necesitas ayuda?

- Revisa `README.md` para documentación general
- Revisa `TECNICO.md` para documentación técnica
- Revisa `EJEMPLOS.py` para ejemplos de código
- Revisa `ESTRUCTURA.txt` para entender la estructura del proyecto

---

**¡Listo! Ahora puedes empezar a crear tu fangame de Rayman. ¡Diviértete! 🎮**
