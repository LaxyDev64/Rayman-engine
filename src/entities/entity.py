"""Entidad base del engine"""

import pygame
from abc import ABC, abstractmethod


class Entity(ABC):
    """Clase base para todas las entidades del juego"""
    
    def __init__(self, x: float, y: float, width: int, height: int):
        """
        Inicializa una entidad
        
        Args:
            x: Posición x
            y: Posición y
            width: Ancho de la entidad
            height: Alto de la entidad
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity_x = 0
        self.velocity_y = 0
        self.active = True
    
    @abstractmethod
    def update(self, dt: float):
        """Actualiza la entidad"""
        pass
    
    @abstractmethod
    def draw(self, surface: pygame.Surface):
        """Dibuja la entidad"""
        pass
    
    def update_rect(self):
        """Actualiza la posición del rectángulo"""
        self.rect.x = self.x
        self.rect.y = self.y
    
    def get_rect(self) -> pygame.Rect:
        """Obtiene el rectángulo de colisión"""
        return self.rect
    
    def set_position(self, x: float, y: float):
        """Establece la posición de la entidad"""
        self.x = x
        self.y = y
        self.update_rect()
    
    def move(self, dx: float, dy: float):
        """Mueve la entidad"""
        self.x += dx
        self.y += dy
        self.update_rect()
