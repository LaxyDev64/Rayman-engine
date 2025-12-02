"""Sistema de colisiones para el engine"""

import pygame
from typing import List, Tuple


class CollisionManager:
    """Gestor de colisiones del juego"""
    
    @staticmethod
    def check_rect_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
        """Verifica colisión entre dos rectángulos"""
        return rect1.colliderect(rect2)
    
    @staticmethod
    def check_point_in_rect(point: Tuple[int, int], rect: pygame.Rect) -> bool:
        """Verifica si un punto está dentro de un rectángulo"""
        return rect.collidepoint(point)
    
    @staticmethod
    def get_collision_direction(moving_rect: pygame.Rect, static_rect: pygame.Rect) -> str:
        """Determina la dirección de colisión"""
        # Calcula la distancia entre los centros
        dx = (moving_rect.centerx - static_rect.centerx)
        dy = (moving_rect.centery - static_rect.centery)
        
        # Calcula el ancho y alto de penetración
        width_penetration = (moving_rect.width + static_rect.width) / 2 - abs(dx)
        height_penetration = (moving_rect.height + static_rect.height) / 2 - abs(dy)
        
        # Retorna la dirección de colisión
        if width_penetration < height_penetration:
            return "left" if dx < 0 else "right"
        else:
            return "top" if dy < 0 else "bottom"
    
    @staticmethod
    def get_nearby_objects(obj_rect: pygame.Rect, objects: List, distance: int = 100) -> List:
        """Obtiene objetos cercanos a una distancia específica"""
        expanded_rect = obj_rect.inflate(distance * 2, distance * 2)
        nearby = []
        for obj in objects:
            if hasattr(obj, 'rect') and expanded_rect.colliderect(obj.rect):
                nearby.append(obj)
        return nearby
