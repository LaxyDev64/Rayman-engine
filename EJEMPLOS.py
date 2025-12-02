"""
EJEMPLOS DE USO DEL RAYMAN ENGINE

Este archivo contiene ejemplos de cómo usar y extender el engine
para crear nuevos niveles, entidades y escenas.
"""

# ============ EJEMPLO 1: Crear un Enemigo Simple ============

from src.entities.entity import Entity
import pygame
from src.config import RED

class SimpleEnemy(Entity):
    """Enemigo que camina de un lado a otro"""
    
    def __init__(self, x: float, y: float, width: int = 30, height: int = 30):
        super().__init__(x, y, width, height)
        self.speed = 2
        self.direction = 1
        self.patrol_range = 200
        self.start_x = x
    
    def update(self, dt: float):
        """Actualiza el enemigo"""
        # Movimiento
        self.x += self.speed * self.direction
        
        # Cambiar dirección si alcanza el rango de patrulla
        if abs(self.x - self.start_x) > self.patrol_range:
            self.direction *= -1
        
        self.update_rect()
    
    def draw(self, surface: pygame.Surface):
        """Dibuja el enemigo"""
        pygame.draw.rect(surface, RED, self.rect)
        pygame.draw.circle(surface, (255, 255, 255), 
                          (self.x + 5, self.y + 5), 3)  # Ojo


# ============ EJEMPLO 2: Plataforma Móvil ============

from src.entities.world import Platform
import math

class MovingPlatform(Platform):
    """Plataforma que se mueve en un patrón"""
    
    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__(x, y, width, height)
        self.start_x = x
        self.start_y = y
        self.time_elapsed = 0
        self.amplitude = 50  # Rango de movimiento
        self.speed = 0.05
    
    def update(self, dt: float):
        """Actualiza la posición con movimiento sinusoidal"""
        self.time_elapsed += dt * self.speed
        
        # Movimiento vertical sinusoidal
        self.y = self.start_y + math.sin(self.time_elapsed) * self.amplitude
        self.update_rect()


# ============ EJEMPLO 3: Nivel Avanzado ============

from src.scenes.level import LevelScene
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT

class AdvancedLevel(LevelScene):
    """Nivel más complejo con múltiples tipos de obstáculos"""
    
    def setup(self):
        """Configura el nivel avanzado"""
        # Llamar setup del padre
        super().setup()
        
        # Añadir enemigos
        enemy1 = SimpleEnemy(400, 400)
        enemy2 = SimpleEnemy(700, 300)
        self.add_entity(enemy1)
        self.add_entity(enemy2)
        
        # Añadir plataformas móviles
        moving_platform = MovingPlatform(500, 250, 150, 20, (100, 200, 100))
        self.add_entity(moving_platform)
        self.platforms.append(moving_platform)
        
        # Crear una sección más difícil
        for i in range(3):
            platform = Platform(200 + i * 100, 500 - i * 60, 80, 20)
            self.add_entity(platform)
            self.platforms.append(platform)


# ============ EJEMPLO 4: Sistema de Vidas ============

class PlayerWithLives:
    """Sistema de vidas para el jugador"""
    
    def __init__(self):
        self.max_lives = 3
        self.current_lives = self.max_lives
    
    def lose_life(self):
        """Pierde una vida"""
        self.current_lives -= 1
        print(f"¡Perdiste una vida! Vidas restantes: {self.current_lives}")
    
    def gain_life(self):
        """Gana una vida"""
        if self.current_lives < self.max_lives:
            self.current_lives += 1
    
    def is_game_over(self) -> bool:
        """Verifica si el juego acabó"""
        return self.current_lives <= 0


# ============ EJEMPLO 5: Contador de Tiempo ============

class TimedLevel(LevelScene):
    """Nivel con limite de tiempo"""
    
    def __init__(self, width: int, height: int, time_limit: float = 120000):
        super().__init__(width, height)
        self.time_limit = time_limit  # en milisegundos
        self.time_elapsed = 0
        self.time_bonus = 0
    
    def update(self, dt: float):
        """Actualiza incluyendo el tiempo"""
        super().update(dt)
        
        self.time_elapsed += dt
        
        # Bonificación por tiempo restante
        if self.time_elapsed < self.time_limit:
            self.time_bonus = int((self.time_limit - self.time_elapsed) / 100)
        else:
            # Tiempo agotado
            self.player.on_fall()
    
    def draw(self, surface: pygame.Surface):
        """Dibuja incluyendo el contador de tiempo"""
        super().draw(surface)
        
        # Mostrar tiempo restante
        font = pygame.font.Font(None, 36)
        time_remaining = max(0, self.time_limit - self.time_elapsed)
        time_text = font.render(
            f"Tiempo: {time_remaining / 1000:.1f}s", 
            True, 
            (255, 255, 0)
        )
        surface.blit(time_text, (SCREEN_WIDTH - 300, 10))


# ============ EJEMPLO 6: Sistema de Puntuaciones ============

class ScoreManager:
    """Gestiona el sistema de puntuación"""
    
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.multiplier = 1
    
    def add_score(self, points: int):
        """Añade puntos"""
        earned = points * self.multiplier
        self.score += earned
        
        if self.score > self.high_score:
            self.high_score = self.score
        
        print(f"+{earned} puntos (x{self.multiplier})")
    
    def set_multiplier(self, multiplier: float):
        """Establece el multiplicador de puntos"""
        self.multiplier = multiplier


# ============ EJEMPLO 7: Usar el Engine Personalizado ============

def example_main():
    """Ejemplo de cómo usar un nivel personalizado"""
    from src.engine import GameEngine
    
    # Crear engine
    game = GameEngine()
    
    # Crear nivel avanzado
    advanced_level = AdvancedLevel(1280, 720)
    game.register_scene("advanced", advanced_level)
    
    # Crear nivel con tiempo
    timed_level = TimedLevel(1280, 720, time_limit=60000)  # 60 segundos
    game.register_scene("timed", timed_level)
    
    # Seleccionar escena
    game.set_scene("advanced")
    
    # Ejecutar
    # game.run()


if __name__ == "__main__":
    print("Este archivo contiene ejemplos de uso.")
    print("No está diseñado para ejecutarse directamente.")
    print("Importa las clases en tus propios scripts.")
