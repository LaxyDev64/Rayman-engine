"""Plataformas y objetos del mundo"""

import pygame
from src.entities.entity import Entity
from src.config import WHITE, GRAY


class Platform(Entity):
    """Plataforma estática"""
    
    def __init__(self, x: float, y: float, width: int, height: int, color=GRAY):
        """Inicializa una plataforma"""
        super().__init__(x, y, width, height)
        self.color = color
    
    def update(self, dt: float):
        """Las plataformas no se actualizan"""
        pass
    
    def draw(self, surface: pygame.Surface):
        """Dibuja la plataforma"""
        pygame.draw.rect(surface, self.color, self.rect)


class Wall(Entity):
    """Pared / obstáculo"""
    
    def __init__(self, x: float, y: float, width: int, height: int):
        """Inicializa una pared"""
        super().__init__(x, y, width, height)
    
    def update(self, dt: float):
        """Las paredes no se actualizan"""
        pass
    
    def draw(self, surface: pygame.Surface):
        """Dibuja la pared"""
        pygame.draw.rect(surface, (100, 50, 50), self.rect)
        pygame.draw.rect(surface, (150, 100, 100), self.rect, 2)


class Spike(Entity):
    """Púa letal"""
    
    def __init__(self, x: float, y: float, size: int = 16):
        """Inicializa una púa"""
        super().__init__(x, y, size, size)
        self.size = size
    
    def update(self, dt: float):
        """Las púas no se actualizan"""
        pass
    
    def draw(self, surface: pygame.Surface):
        """Dibuja la púa"""
        points = [
            (self.x + self.size // 2, self.y),
            (self.x + self.size, self.y + self.size),
            (self.x, self.y + self.size)
        ]
        pygame.draw.polygon(surface, (200, 0, 0), points)


class Collectible(Entity):
    """Objeto coleccionable (frutas, monedas, etc.)"""
    
    def __init__(self, x: float, y: float, value: int = 10):
        """Inicializa un objeto coleccionable"""
        super().__init__(x, y, 16, 16)
        self.value = value
        self.collected = False
    
    def update(self, dt: float):
        """Anima el objeto coleccionable"""
        self.y += 0.5 * (1 if int(dt) % 2 == 0 else -1)  # Efecto de flotación
        self.update_rect()
    
    def draw(self, surface: pygame.Surface):
        """Dibuja el objeto coleccionable"""
        if not self.collected:
            pygame.draw.circle(surface, (255, 215, 0), (self.x + 8, self.y + 8), 6)
            pygame.draw.circle(surface, (200, 170, 0), (self.x + 8, self.y + 8), 6, 2)
