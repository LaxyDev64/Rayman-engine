"""Archivo principal del juego"""

import sys
import os

# Añadir directorio actual a sys.path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.engine import GameEngine
from src.scenes.level import LevelScene


def main():
    """Función principal"""
    # Crear el motor del juego
    game = GameEngine()
    
    # Crear y registrar escenas
    level_scene = LevelScene(1280, 720)
    game.register_scene("level_1", level_scene)
    
    # Establecer la escena inicial
    game.set_scene("level_1")
    
    # Ejecutar el juego
    game.run()


if __name__ == "__main__":
    main()
