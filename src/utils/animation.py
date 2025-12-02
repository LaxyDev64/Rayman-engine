"""Sistema de animaciones para el engine"""

import pygame
from typing import List, Dict


class Animation:
    """Clase para manejar animaciones de sprites"""
    
    def __init__(self, frames: List[pygame.Surface], frame_duration: int = 10, loop: bool = True):
        """
        Inicializa una animación
        
        Args:
            frames: Lista de superficies (imágenes) de la animación
            frame_duration: Duración de cada frame en milisegundos
            loop: Si la animación debe repetirse
        """
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.elapsed_time = 0
        self.finished = False
    
    def update(self, dt: int) -> pygame.Surface:
        """
        Actualiza la animación
        
        Args:
            dt: Delta de tiempo en milisegundos
        
        Returns:
            El frame actual de la animación
        """
        if self.finished and not self.loop:
            return self.frames[-1]
        
        self.elapsed_time += dt
        
        if self.elapsed_time >= self.frame_duration:
            self.elapsed_time = 0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
        
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reinicia la animación"""
        self.current_frame = 0
        self.elapsed_time = 0
        self.finished = False


class AnimationController:
    """Controlador de múltiples animaciones"""
    
    def __init__(self):
        """Inicializa el controlador de animaciones"""
        self.animations: Dict[str, Animation] = {}
        self.current_animation = None
    
    def add_animation(self, name: str, animation: Animation):
        """Añade una nueva animación"""
        self.animations[name] = animation
    
    def play(self, name: str):
        """Reproduce una animación"""
        if name in self.animations:
            if self.current_animation != name:
                if self.current_animation:
                    self.animations[self.current_animation].reset()
                self.current_animation = name
    
    def update(self, dt: int) -> pygame.Surface:
        """Actualiza la animación actual"""
        if self.current_animation and self.current_animation in self.animations:
            return self.animations[self.current_animation].update(dt)
        return None
    
    def get_current_animation_name(self) -> str:
        """Obtiene el nombre de la animación actual"""
        return self.current_animation
