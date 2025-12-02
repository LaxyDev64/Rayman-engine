"""
PRUEBAS DEL ENGINE

Archivo para ejecutar pruebas básicas del engine
"""

import sys
import os

# Añadir el directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que todos los módulos se importan correctamente"""
    print("Probando importaciones...")
    
    try:
        from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
        print("✓ Config importado")
        
        from src.engine import GameEngine
        print("✓ Engine importado")
        
        from src.entities.entity import Entity
        from src.entities.player import Player
        from src.entities.world import Platform, Wall, Spike, Collectible
        print("✓ Entidades importadas")
        
        from src.scenes.scene import Scene
        from src.scenes.level import LevelScene
        print("✓ Escenas importadas")
        
        from src.utils.collision import CollisionManager
        from src.utils.animation import Animation, AnimationController
        print("✓ Utilidades importadas")
        
        print("\n✓ Todas las importaciones exitosas!")
        return True
    
    except Exception as e:
        print(f"✗ Error en importación: {e}")
        return False


def test_player_creation():
    """Prueba la creación del jugador"""
    print("\nProbando creación del jugador...")
    
    try:
        from src.entities.player import Player
        
        player = Player(100, 100)
        assert player.x == 100
        assert player.y == 100
        assert player.direction == 1
        print("✓ Jugador creado correctamente")
        return True
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_collision():
    """Prueba el sistema de colisiones"""
    print("\nProbando sistema de colisiones...")
    
    try:
        import pygame
        from src.utils.collision import CollisionManager
        
        rect1 = pygame.Rect(0, 0, 100, 100)
        rect2 = pygame.Rect(50, 50, 100, 100)
        
        assert CollisionManager.check_rect_collision(rect1, rect2) == True
        print("✓ Colisión detectada correctamente")
        
        rect3 = pygame.Rect(200, 200, 100, 100)
        assert CollisionManager.check_rect_collision(rect1, rect3) == False
        print("✓ No-colisión detectada correctamente")
        
        return True
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_level_creation():
    """Prueba la creación de un nivel"""
    print("\nProbando creación de nivel...")
    
    try:
        from src.scenes.level import LevelScene
        
        level = LevelScene(1280, 720)
        assert level.player is not None
        assert len(level.platforms) > 0
        print(f"✓ Nivel creado con {len(level.platforms)} plataformas")
        return True
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_enemy_interaction():
    """Prueba interacción entre jugador y enemigo (salto sobre enemigo)"""
    print("\nProbando interacción jugador-enemigo...")
    try:
        from src.scenes.level import LevelScene
        from src.entities.enemy import SimpleEnemy
        
        level = LevelScene(1280, 720)
        # Crear un enemigo y colocarlo en el nivel
        enemy = SimpleEnemy(400, 720 - 82, patrol_range=50, speed=0)
        level.add_entity(enemy)
        level.enemies.append(enemy)

        # Posicionar al jugador justo encima del enemigo y forzar caída
        player = level.player
        player.set_position(enemy.x, enemy.y - player.height - 2)
        player.velocity_y = 5

        # Ejecutar varias actualizaciones cortas para simular la caída
        for _ in range(5):
            level.update(50)

        # Verificar que el enemigo fue golpeado (muerto) por el jugador
        if not enemy.active:
            print("✓ Jugador aplastó al enemigo correctamente")
            return True
        else:
            print("✗ El enemigo no murió; revisa la lógica de colisiones")
            return False

    except Exception as e:
        print(f"✗ Error en test_enemy_interaction: {e}")
        return False


def main():
    """Ejecuta todas las pruebas"""
    print("=" * 50)
    print("PRUEBAS DEL RAYMAN ENGINE")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_player_creation,
        test_collision,
        test_level_creation
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print(f"Resultados: {sum(results)}/{len(results)} pruebas pasadas")
    print("=" * 50)
    
    if all(results):
        print("\n✓ ¡Todas las pruebas pasaron! El engine está listo.")
        return 0
    else:
        print("\n✗ Algunas pruebas fallaron. Revisa los errores arriba.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
