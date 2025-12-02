"""Sistema de escenas del juego"""

import pygame
from abc import ABC, abstractmethod
from typing import List
from src.entities.entity import Entity


class Scene(ABC):
    """Clase base para todas las escenas del juego"""
    
    def __init__(self, width: int, height: int):
        """
        Inicializa una escena
        
        Args:
            width: Ancho de la pantalla
            height: Alto de la pantalla
        """
        self.width = width
        self.height = height
        self.entities: List[Entity] = []
        self.active = True
        self.background_color = (50, 50, 50)
    
    @abstractmethod
    def setup(self):
        """Configura la escena (entidades, etc.)"""
        pass
    
    @abstractmethod
    def handle_input(self, event: pygame.event.Event):
        """Maneja la entrada del usuario"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """Actualiza la escena"""
        pass
    
    @abstractmethod
    def draw(self, surface: pygame.Surface):
        """Dibuja la escena"""
        pass
    
    def add_entity(self, entity: Entity):
        """Añade una entidad a la escena"""
        self.entities.append(entity)
    
    def remove_entity(self, entity: Entity):
        """Elimina una entidad de la escena"""
        if entity in self.entities:
            self.entities.remove(entity)
    
    def get_entities_by_type(self, entity_type: type) -> List[Entity]:
        """Obtiene todas las entidades de un tipo específico"""
        return [e for e in self.entities if isinstance(e, entity_type)]
