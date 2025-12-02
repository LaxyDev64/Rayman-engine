"""Motor principal del juego"""

import pygame
import sys
from typing import Dict
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE, BLACK
from src.scenes.scene import Scene


class GameEngine:
    """Motor principal del juego Rayman"""
    
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT, title: str = GAME_TITLE):
        """
        Inicializa el motor del juego
        
        Args:
            width: Ancho de la pantalla
            height: Alto de la pantalla
            title: Título de la ventana
        """
        self.width = width
        self.height = height
        self.title = title
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = None
        self.scenes: Dict[str, Scene] = {}
        self.current_scene_name = None
        self.current_scene = None
        self.fps = FPS
        self.dt = 0
    
    def initialize(self):
        """Inicializa Pygame y la pantalla"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        print(f"[ENGINE] Inicializado: {self.width}x{self.height} - {self.title}")
    
    def register_scene(self, name: str, scene: Scene):
        """Registra una escena"""
        self.scenes[name] = scene
        print(f"[ENGINE] Escena registrada: {name}")
    
    def set_scene(self, name: str):
        """Cambia a una escena específica"""
        if name in self.scenes:
            self.current_scene_name = name
            self.current_scene = self.scenes[name]
            print(f"[ENGINE] Escena activa: {name}")
        else:
            print(f"[ENGINE] ERROR: Escena '{name}' no encontrada")
    
    def handle_events(self):
        """Maneja los eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.current_scene:
                self.current_scene.handle_input(event)
    
    def update(self):
        """Actualiza la lógica del juego"""
        if self.current_scene and self.current_scene.active:
            self.current_scene.update(self.dt)
    
    def draw(self):
        """Dibuja la pantalla"""
        self.screen.fill(BLACK)
        
        if self.current_scene:
            self.current_scene.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Bucle principal del juego"""
        self.initialize()
        
        while self.running:
            self.dt = self.clock.tick(self.fps)
            
            self.handle_events()
            self.update()
            self.draw()
        
        self.quit()
    
    def quit(self):
        """Sale del juego"""
        pygame.quit()
        sys.exit()
        print("[ENGINE] Juego finalizado")
